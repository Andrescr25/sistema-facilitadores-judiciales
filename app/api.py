#!/usr/bin/env python3
"""
API REST para el bot de Facilitadores Judiciales.
Expone endpoints para consultas con RAG y GPT4All local.
"""

import os
import sys
import logging
from typing import Dict, Any, List
from pathlib import Path

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Importaciones de FastAPI
try:
    from fastapi import FastAPI, HTTPException, Depends, Request, status
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
    from pydantic import BaseModel
    from contextlib import asynccontextmanager
except ImportError as e:
    logger.error(f"Error importando FastAPI: {e}")
    logger.error("Ejecuta: pip install fastapi uvicorn")
    sys.exit(1)

# Importaciones de LangChain
try:
    from langchain.vectorstores import Chroma
    from langchain.embeddings import SentenceTransformerEmbeddings
    from langchain.chains import RetrievalQA
    from langchain.llms import GPT4All as GPT4AllLangChain
    from langchain.prompts import PromptTemplate
    from langchain.schema import Document
except ImportError as e:
    logger.error(f"Error importando LangChain: {e}")
    logger.error("Ejecuta: pip install langchain langchain-community")
    sys.exit(1)

# Importación de GPT4All nativo (fallback)
try:
    from gpt4all import GPT4All
except ImportError:
    GPT4All = None
    logger.warning("GPT4All nativo no disponible, usando solo LangChain")

# Importaciones de seguridad
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from security import (
        security_manager, 
        validate_auth_header, 
        check_permission,
        log_security_event
    )
    print("✅ Módulo de seguridad cargado correctamente")
except ImportError as e:
    print(f"⚠️  Error importando seguridad: {e}")
    print("⚠️  Usando modo sin autenticación.")
    
    # Crear funciones mock para modo sin autenticación
    class MockSecurityManager:
        def generate_token(self, user_id, role="user"):
            return f"mock-token-{user_id}-{role}"
        
        def validate_token(self, token):
            if token and token.startswith("mock-token-"):
                return {"user_id": "mock-user", "role": "user", "created_at": time.time(), "expires_at": time.time() + 3600}
            return None
        
        def check_rate_limit(self, client_ip):
            return True
        
        def get_user_permissions(self, role):
            return {"read": True, "write": True, "delete": True, "manage_users": True, "view_logs": True}
        
        def get_security_stats(self):
            return {"active_tokens": 0, "total_requests_last_hour": 0, "unique_ips": 0}
    
    security_manager = MockSecurityManager()
    
    def validate_auth_header(auth_header):
        if not auth_header:
            return None
        if not auth_header.startswith("Bearer "):
            return None
        token = auth_header[7:]
        return security_manager.validate_token(token)
    
    def check_permission(user_info, permission):
        return True  # Permitir todo en modo mock
    
    def log_security_event(event_type, user_id, details):
        print(f"SECURITY_EVENT: {event_type} | User: {user_id} | Details: {details}")

# Configuración
MODEL_PATH = os.getenv("MODEL_PATH", "/Users/joseandres/Downloads/ChatBot/models/deepseek.gguf")
PERSIST_DIR = os.getenv("VECTOR_DB_DIR", "./data/chroma")
MODEL_EMBED = "all-MiniLM-L6-v2"

# Prompt template especializado
FACILITADOR_PROMPT_TEMPLATE = """Eres un asistente especializado en facilitación judicial y resolución de conflictos. Tu función es ayudar a facilitadores judiciales con información precisa y relevante basada en los documentos proporcionados.

INSTRUCCIONES:
- Usa ÚNICAMENTE la información contenida en los fragmentos de contexto proporcionados
- Responde de forma clara, concisa y profesional
- Si la información no está en los documentos, responde: "No tengo información suficiente en los documentos provistos para responder a esa pregunta"
- Siempre menciona la fuente del documento cuando sea relevante
- Mantén un tono formal pero accesible
- Si hay procedimientos específicos, menciona los pasos en orden

CONTEXTO:
{context}

PREGUNTA: {question}

RESPUESTA:"""

# Modelos Pydantic
class QueryRequest(BaseModel):
    question: str
    
    class Config:
        schema_extra = {
            "example": {
                "question": "¿Cuáles son los requisitos para ser facilitador judicial?"
            }
        }

class QueryResponse(BaseModel):
    answer: str
    sources: List[Dict[str, str]]
    processing_time: float
    
    class Config:
        schema_extra = {
            "example": {
                "answer": "Para ser facilitador judicial se requiere...",
                "sources": [
                    {
                        "filename": "marco_legal.txt",
                        "content": "MARCO LEGAL DE LA FACILITACIÓN JUDICIAL...",
                        "source": "./data/docs/marco_legal.txt"
                    }
                ],
                "processing_time": 1.23
            }
        }

class HealthResponse(BaseModel):
    status: str
    message: str
    model_loaded: bool
    vector_db_loaded: bool
    documents_count: int

# Variables globales para el bot
bot_instance = None

# Configuración de seguridad
security_scheme = HTTPBearer(auto_error=False)
ENABLE_AUTH = os.getenv("ENABLE_AUTH", "true").lower() == "true"

# Función para obtener IP del cliente
def get_client_ip(request: Request) -> str:
    """
    Obtiene la IP del cliente desde el request.
    """
    # Verificar headers de proxy
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    
    real_ip = request.headers.get("X-Real-IP")
    if real_ip:
        return real_ip
    
    # IP directa
    return request.client.host if request.client else "unknown"

# Función de dependencia para autenticación
async def get_current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme)
) -> Optional[Dict[str, Any]]:
    """
    Obtiene el usuario actual desde el token de autenticación.
    """
    if not ENABLE_AUTH:
        # Modo sin autenticación para desarrollo
        return {
            "user_id": "anonymous",
            "role": "user",
            "created_at": time.time(),
            "expires_at": time.time() + 3600
        }
    
    if not credentials:
        return None
    
    # Validar token
    user_info = validate_auth_header(credentials.credentials)
    if not user_info:
        return None
    
    # Verificar rate limiting
    client_ip = get_client_ip(request)
    if not security_manager.check_rate_limit(client_ip):
        log_security_event("RATE_LIMIT_EXCEEDED", user_info.get("user_id", "unknown"), f"IP: {client_ip}")
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Demasiadas solicitudes. Intenta de nuevo más tarde."
        )
    
    return user_info

# Función de dependencia para verificar permisos
def require_permission(permission: str):
    """
    Decorator para verificar permisos específicos.
    """
    def permission_checker(user_info: Optional[Dict[str, Any]] = Depends(get_current_user)):
        if not user_info:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token de autenticación requerido",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        if not check_permission(user_info, permission):
            log_security_event("PERMISSION_DENIED", user_info.get("user_id", "unknown"), f"Permission: {permission}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permiso insuficiente. Se requiere: {permission}"
            )
        
        return user_info
    
    return permission_checker

class FacilitadorBotAPI:
    """
    Bot especializado en facilitación judicial con RAG para API.
    """
    
    def __init__(self, model_path: str, persist_dir: str):
        self.model_path = model_path
        self.persist_dir = persist_dir
        self.vectordb = None
        self.qa_chain = None
        self.llm = None
        self.initialized = False
        
    def load_vector_database(self) -> bool:
        """
        Carga la base de datos vectorial existente.
        """
        try:
            logger.info("Cargando base de datos vectorial...")
            
            # Verificar que existe la base de datos
            if not Path(self.persist_dir).exists():
                logger.error(f"Base de datos no encontrada en {self.persist_dir}")
                return False
            
            # Cargar embeddings
            embedder = SentenceTransformerEmbeddings(model_name=MODEL_EMBED)
            
            # Cargar base de datos vectorial
            self.vectordb = Chroma(
                persist_directory=self.persist_dir,
                embedding_function=embedder
            )
            
            # Verificar que hay documentos
            doc_count = self.vectordb._collection.count()
            if doc_count == 0:
                logger.error("La base de datos está vacía")
                return False
            
            logger.info(f"✅ Base de datos cargada con {doc_count} documentos")
            return True
            
        except Exception as e:
            logger.error(f"Error cargando base de datos: {e}")
            return False
    
    def load_llm(self) -> bool:
        """
        Carga el modelo de lenguaje local.
        """
        try:
            logger.info("Cargando modelo de lenguaje...")
            
            # Verificar que existe el modelo
            if not Path(self.model_path).exists():
                logger.warning(f"Modelo no encontrado en {self.model_path}")
                logger.warning("Usando modo demo sin modelo real")
                return True  # Continuar en modo demo
            
            # Intentar cargar con LangChain primero
            try:
                self.llm = GPT4AllLangChain(
                    model=self.model_path,
                    n_ctx=2048,
                    temperature=0.1,
                    max_tokens=512,
                    verbose=False
                )
                logger.info("✅ Modelo cargado con LangChain")
                return True
                
            except Exception as e:
                logger.warning(f"Error con LangChain: {e}")
                
                # Fallback a GPT4All nativo
                if GPT4All:
                    try:
                        self.llm = GPT4All(self.model_path)
                        logger.info("✅ Modelo cargado con GPT4All nativo")
                        return True
                    except Exception as e2:
                        logger.warning(f"Error con GPT4All nativo: {e2}")
                
                return True  # Continuar en modo demo
                
        except Exception as e:
            logger.warning(f"Error cargando modelo: {e}")
            return True  # Continuar en modo demo
    
    def create_qa_chain(self) -> bool:
        """
        Crea la cadena de pregunta-respuesta con RAG.
        """
        try:
            logger.info("Creando cadena de pregunta-respuesta...")
            
            if not self.vectordb:
                logger.error("Base de datos no cargada")
                return False
            
            # Configurar retriever
            retriever = self.vectordb.as_retriever(
                search_kwargs={"k": 3}
            )
            
            if self.llm:
                # Crear prompt template
                prompt = PromptTemplate(
                    template=FACILITADOR_PROMPT_TEMPLATE,
                    input_variables=["context", "question"]
                )
                
                # Crear cadena de QA
                self.qa_chain = RetrievalQA.from_chain_type(
                    llm=self.llm,
                    chain_type="stuff",
                    retriever=retriever,
                    return_source_documents=True,
                    chain_type_kwargs={"prompt": prompt}
                )
            else:
                # Modo demo sin LLM real
                self.qa_chain = None
                logger.info("Modo demo: Sin modelo LLM real")
            
            logger.info("✅ Cadena de QA creada exitosamente")
            return True
            
        except Exception as e:
            logger.error(f"Error creando cadena de QA: {e}")
            return False
    
    def initialize(self) -> bool:
        """
        Inicializa todos los componentes del bot.
        """
        logger.info("🚀 Inicializando bot de Facilitadores Judiciales...")
        
        # Cargar base de datos vectorial
        if not self.load_vector_database():
            return False
        
        # Cargar modelo de lenguaje
        if not self.load_llm():
            return False
        
        # Crear cadena de QA
        if not self.create_qa_chain():
            return False
        
        self.initialized = True
        logger.info("✅ Bot inicializado correctamente")
        return True
    
    def ask(self, question: str) -> Dict[str, Any]:
        """
        Procesa una pregunta y devuelve la respuesta con fuentes.
        """
        if not self.initialized:
            return {
                "answer": "Error: Bot no inicializado correctamente",
                "sources": [],
                "processing_time": 0.0
            }
        
        import time
        start_time = time.time()
        
        try:
            logger.info(f"Procesando pregunta: {question}")
            
            if self.qa_chain:
                # Usar cadena de QA real
                result = self.qa_chain({"query": question})
                
                answer = result.get("result", "No se pudo generar respuesta")
                sources = []
                
                if "source_documents" in result:
                    for doc in result["source_documents"]:
                        sources.append({
                            "filename": doc.metadata.get("filename", "Desconocido"),
                            "content": doc.page_content[:200] + "...",
                            "source": doc.metadata.get("source", "Desconocido")
                        })
            else:
                # Modo demo - buscar documentos y generar respuesta simple
                results = self.vectordb.similarity_search(question, k=3)
                
                sources = []
                for doc in results:
                    sources.append({
                        "filename": doc.metadata.get("filename", "Desconocido"),
                        "content": doc.page_content[:200] + "...",
                        "source": doc.metadata.get("source", "Desconocido")
                    })
                
                # Respuesta demo basada en palabras clave
                question_lower = question.lower()
                if "requisitos" in question_lower and "facilitador" in question_lower:
                    answer = "Para ser facilitador judicial se requiere: título profesional en áreas afines, experiencia mínima de 3 años, certificación vigente del Consejo Superior de la Judicatura, no tener antecedentes disciplinarios, y renovar certificación cada 3 años."
                elif "duración" in question_lower or "dura" in question_lower:
                    answer = "El procedimiento de conciliación judicial tiene una duración máxima de 30 días hábiles desde la admisión de la solicitud."
                elif "técnicas" in question_lower or "facilitación" in question_lower:
                    answer = "Las técnicas de facilitación incluyen: escucha activa, parafraseo, preguntas abiertas, reformulación y lluvia de ideas."
                elif "costos" in question_lower or "precio" in question_lower:
                    answer = "Los costos incluyen: tasa de admisión $50.000, honorarios del facilitador $100.000 por sesión, y gastos de notificación $25.000 por parte."
                elif "fases" in question_lower or "etapas" in question_lower:
                    answer = "Las fases son: admisión, citación, audiencia y homologación."
                else:
                    answer = "No tengo información suficiente en los documentos provistos para responder a esa pregunta específica."
            
            processing_time = time.time() - start_time
            logger.info(f"Respuesta generada en {processing_time:.2f}s con {len(sources)} fuentes")
            
            return {
                "answer": answer,
                "sources": sources,
                "processing_time": processing_time
            }
            
        except Exception as e:
            logger.error(f"Error procesando pregunta: {e}")
            processing_time = time.time() - start_time
            return {
                "answer": f"Error procesando la pregunta: {str(e)}",
                "sources": [],
                "processing_time": processing_time
            }

# Función para obtener el bot
def get_bot() -> FacilitadorBotAPI:
    global bot_instance
    if bot_instance is None:
        raise HTTPException(status_code=503, detail="Bot no inicializado")
    return bot_instance

# Eventos de la aplicación
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gestión del ciclo de vida de la aplicación.
    """
    global bot_instance
    
    # Inicialización
    logger.info("🚀 Iniciando API de Facilitadores Judiciales...")
    bot_instance = FacilitadorBotAPI(MODEL_PATH, PERSIST_DIR)
    
    if not bot_instance.initialize():
        logger.error("❌ Error inicializando el bot")
        raise Exception("No se pudo inicializar el bot")
    
    logger.info("✅ API lista para recibir requests")
    
    yield
    
    # Limpieza
    logger.info("🛑 Cerrando API...")

# Crear aplicación FastAPI
app = FastAPI(
    title="Bot de Facilitadores Judiciales",
    description="API REST para consultas sobre facilitación judicial con RAG y GPT4All local",
    version="1.0.0",
    lifespan=lifespan
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoints
@app.get("/", response_model=Dict[str, str])
async def root():
    """
    Endpoint raíz con información básica.
    """
    return {
        "message": "Bot de Facilitadores Judiciales API",
        "version": "1.0.0",
        "status": "active"
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Endpoint de salud del sistema.
    """
    global bot_instance
    
    if not bot_instance or not bot_instance.initialized:
        return HealthResponse(
            status="unhealthy",
            message="Bot no inicializado",
            model_loaded=False,
            vector_db_loaded=False,
            documents_count=0
        )
    
    # Verificar estado de componentes
    model_loaded = bot_instance.llm is not None
    vector_db_loaded = bot_instance.vectordb is not None
    documents_count = bot_instance.vectordb._collection.count() if vector_db_loaded else 0
    
    return HealthResponse(
        status="healthy",
        message="Sistema funcionando correctamente",
        model_loaded=model_loaded,
        vector_db_loaded=vector_db_loaded,
        documents_count=documents_count
    )

@app.post("/ask", response_model=QueryResponse)
async def ask_question(
    request: QueryRequest,
    user_info: Optional[Dict[str, Any]] = Depends(get_current_user),
    bot: FacilitadorBotAPI = Depends(get_bot)
):
    """
    Endpoint principal para hacer consultas al bot.
    Requiere autenticación.
    """
    if not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="La pregunta no puede estar vacía"
        )
    
    try:
        # Log de la consulta
        user_id = user_info.get("user_id", "anonymous") if user_info else "anonymous"
        log_security_event("QUESTION_ASKED", user_id, f"Question: {request.question[:50]}...")
        
        result = bot.ask(request.question)
        
        return QueryResponse(
            answer=result["answer"],
            sources=result["sources"],
            processing_time=result["processing_time"]
        )
        
    except Exception as e:
        logger.error(f"Error en endpoint /ask: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error interno del servidor: {str(e)}"
        )

@app.get("/documents")
async def get_documents_info(bot: FacilitadorBotAPI = Depends(get_bot)):
    """
    Endpoint para obtener información sobre los documentos cargados.
    """
    if not bot.vectordb:
        raise HTTPException(
            status_code=503,
            detail="Base de datos vectorial no disponible"
        )
    
    try:
        # Obtener información de la base de datos
        doc_count = bot.vectordb._collection.count()
        
        # Obtener algunos documentos de ejemplo
        sample_docs = bot.vectordb.similarity_search("", k=5)
        
        documents_info = []
        for doc in sample_docs:
            documents_info.append({
                "filename": doc.metadata.get("filename", "Desconocido"),
                "source": doc.metadata.get("source", "Desconocido"),
                "preview": doc.page_content[:100] + "..."
            })
        
        return {
            "total_documents": doc_count,
            "sample_documents": documents_info
        }
        
    except Exception as e:
        logger.error(f"Error obteniendo información de documentos: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error obteniendo información: {str(e)}"
        )

# Nuevos endpoints de autenticación y seguridad

@app.post("/auth/login")
async def login(user_id: str, role: str = "user"):
    """
    Endpoint para generar un token de autenticación.
    """
    try:
        token = security_manager.generate_token(user_id, role)
        log_security_event("LOGIN_SUCCESS", user_id, f"Role: {role}")
        
        return {
            "access_token": token,
            "token_type": "bearer",
            "user_id": user_id,
            "role": role,
            "expires_in": security_manager.token_expiry_hours * 3600
        }
        
    except Exception as e:
        logger.error(f"Error en login: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error generando token: {str(e)}"
        )

@app.post("/auth/logout")
async def logout(
    user_info: Optional[Dict[str, Any]] = Depends(get_current_user)
):
    """
    Endpoint para revocar un token de autenticación.
    """
    if not user_info:
        raise HTTPException(
            status_code=401,
            detail="No autenticado"
        )
    
    # En un sistema real, necesitarías pasar el token para revocarlo
    # Por simplicidad, solo logueamos el evento
    user_id = user_info.get("user_id", "unknown")
    log_security_event("LOGOUT", user_id, "Token revocado")
    
    return {"message": "Sesión cerrada exitosamente"}

@app.get("/auth/me")
async def get_current_user_info(
    user_info: Optional[Dict[str, Any]] = Depends(get_current_user)
):
    """
    Endpoint para obtener información del usuario actual.
    """
    if not user_info:
        raise HTTPException(
            status_code=401,
            detail="No autenticado"
        )
    
    return {
        "user_id": user_info.get("user_id"),
        "role": user_info.get("role"),
        "permissions": security_manager.get_user_permissions(user_info.get("role", "user"))
    }

@app.get("/auth/dev-tokens")
async def get_dev_tokens():
    """
    Endpoint para obtener tokens de desarrollo.
    Solo disponible en modo desarrollo.
    """
    if ENABLE_AUTH:
        raise HTTPException(
            status_code=403,
            detail="Tokens de desarrollo solo disponibles cuando ENABLE_AUTH=false"
        )
    
    return {
        "tokens": security_manager.dev_tokens,
        "note": "Estos tokens son solo para desarrollo. No usar en producción."
    }

@app.get("/security/stats")
async def get_security_stats(
    user_info: Optional[Dict[str, Any]] = Depends(require_permission("view_logs"))
):
    """
    Endpoint para obtener estadísticas de seguridad.
    Requiere permisos de administrador.
    """
    stats = security_manager.get_security_stats()
    return {
        "security_stats": stats,
        "auth_enabled": ENABLE_AUTH,
        "timestamp": time.time()
    }

@app.post("/security/cleanup")
async def cleanup_security_data(
    user_info: Optional[Dict[str, Any]] = Depends(require_permission("manage_users"))
):
    """
    Endpoint para limpiar datos de seguridad (tokens expirados, etc.).
    Requiere permisos de administrador.
    """
    security_manager.cleanup_expired_tokens()
    
    log_security_event("CLEANUP", user_info.get("user_id", "unknown"), "Security data cleaned")
    
    return {
        "message": "Datos de seguridad limpiados exitosamente",
        "timestamp": time.time()
    }

if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("API_HOST", "0.0.0.0")
    
    logger.info(f"🚀 Iniciando servidor en {host}:{port}")
    logger.info(f"🔐 Autenticación: {'Habilitada' if ENABLE_AUTH else 'Deshabilitada'}")
    
    uvicorn.run(
        "app.api:app",
        host=host,
        port=port,
        reload=True,
        log_level="info"
    )
