#!/usr/bin/env python3
"""
API simplificada para el bot de Facilitadores Judiciales con autenticación básica.
"""

import os
import sys
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import time

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
    sys.exit(1)

# Importaciones de LangChain
try:
    from langchain.vectorstores import Chroma
    from langchain.embeddings import SentenceTransformerEmbeddings
    from langchain.schema import Document
except ImportError as e:
    logger.error(f"Error importando LangChain: {e}")
    sys.exit(1)

# Configuración
MODEL_PATH = os.getenv("MODEL_PATH", "/Users/joseandres/Downloads/ChatBot/models/DeepSeek-R1-Distill-Llama-8B-Q4_0.gguf")
PERSIST_DIR = os.getenv("VECTOR_DB_DIR", "./data/chroma")
MODEL_EMBED = "all-MiniLM-L6-v2"
ENABLE_AUTH = os.getenv("ENABLE_AUTH", "true").lower() == "true"

# Modelos Pydantic
class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str
    sources: List[Dict[str, str]]
    processing_time: float

class LoginRequest(BaseModel):
    user_id: str
    role: str = "user"

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str
    role: str
    expires_in: int

# Sistema de autenticación simple
class SimpleAuth:
    def __init__(self):
        self.tokens = {}
        self.dev_tokens = {
            "admin": "dev-admin-token-12345",
            "user": "dev-user-token-67890",
            "facilitador": "dev-facilitador-token-abcde"
        }
    
    def generate_token(self, user_id: str, role: str) -> str:
        token = f"token-{user_id}-{role}-{int(time.time())}"
        self.tokens[token] = {
            "user_id": user_id,
            "role": role,
            "created_at": time.time(),
            "expires_at": time.time() + 86400  # 24 horas
        }
        return token
    
    def validate_token(self, token: str) -> Optional[Dict[str, Any]]:
        if not token:
            return None
        
        # Verificar tokens generados
        if token in self.tokens:
            payload = self.tokens[token]
            if time.time() > payload["expires_at"]:
                del self.tokens[token]
                return None
            return payload
        
        # Verificar tokens de desarrollo
        if token in self.dev_tokens.values():
            for user_id, dev_token in self.dev_tokens.items():
                if dev_token == token:
                    return {
                        "user_id": user_id,
                        "role": "admin" if user_id == "admin" else "user",
                        "created_at": time.time() - 3600,
                        "expires_at": time.time() + 86400
                    }
        
        return None

# Instancia de autenticación
auth = SimpleAuth()

# Bot simple
class SimpleBot:
    def __init__(self):
        self.vectordb = None
        self.model = None
        self.initialized = False
    
    def load_vector_database(self) -> bool:
        try:
            logger.info("Cargando base de datos vectorial...")
            
            if not os.path.exists(PERSIST_DIR):
                logger.error(f"Base de datos no encontrada en {PERSIST_DIR}")
                return False
            
            embedder = SentenceTransformerEmbeddings(model_name=MODEL_EMBED)
            self.vectordb = Chroma(
                persist_directory=PERSIST_DIR,
                embedding_function=embedder
            )
            
            doc_count = self.vectordb._collection.count()
            if doc_count == 0:
                logger.error("La base de datos está vacía")
                return False
            
            logger.info(f"✅ Base de datos cargada con {doc_count} documentos")
            return True
            
        except Exception as e:
            logger.error(f"Error cargando base de datos: {e}")
            return False
    
    def load_model(self) -> bool:
        """Carga el modelo GPT4All una sola vez."""
        try:
            if os.path.exists(MODEL_PATH):
                logger.info("🔄 Cargando modelo GPT4All...")
                from gpt4all import GPT4All
                self.model = GPT4All(MODEL_PATH, device='cpu')
                logger.info("✅ Modelo GPT4All cargado en memoria")
                return True
            else:
                logger.warning(f"Modelo GPT4All no encontrado en {MODEL_PATH}")
                return False
        except Exception as e:
            logger.error(f"❌ Error cargando modelo GPT4All: {e}")
            return False
    
    def ask(self, question: str) -> Dict[str, Any]:
        if not self.initialized or not self.vectordb:
            return {
                "answer": "Error: Bot no inicializado",
                "sources": [],
                "processing_time": 0.0
            }
        
        start_time = time.time()
        
        try:
            # Buscar documentos relevantes
            results = self.vectordb.similarity_search(question, k=3)
            
            sources = []
            for doc in results:
                sources.append({
                    "filename": doc.metadata.get("filename", "Desconocido"),
                    "content": doc.page_content[:200] + "...",
                    "source": doc.metadata.get("source", "Desconocido")
                })
            
            # Crear contexto con los documentos encontrados
            context = "\n\n".join([doc.page_content for doc in results])
            
            # Prompt para GPT4All
            prompt = f"""Eres un asistente especializado en facilitación judicial en Colombia. Tu función es ayudar a facilitadores judiciales y ciudadanos con consultas sobre procedimientos de conciliación, requisitos legales y técnicas de facilitación.

CONTEXTO (información disponible):
{context}

PREGUNTA: {question}

INSTRUCCIONES:
- Responde basándote en la información del contexto
- Si la pregunta es sobre facilitación judicial pero no está en el contexto, proporciona orientación general
- Si la pregunta no es sobre facilitación judicial, explica que tu especialidad es la facilitación judicial
- Sé claro, conciso y profesional
- Si hay información relevante en el contexto, úsala para responder

RESPUESTA:"""
            
            # Usar GPT4All si está disponible
            if self.model:
                try:
                    logger.info("🔄 Generando respuesta con modelo cargado...")
                    answer = self.model.generate(prompt, max_tokens=500, temp=0.1)
                    logger.info("✅ Respuesta generada con GPT4All")
                except Exception as e:
                    logger.error(f"❌ Error con GPT4All: {e}")
                    logger.warning("Usando respuesta de fallback")
                    answer = self._get_fallback_answer(question, context)
            else:
                logger.warning("Modelo GPT4All no cargado, usando respuesta de fallback")
                answer = self._get_fallback_answer(question, context)
            
            processing_time = time.time() - start_time
            
            return {
                "answer": answer,
                "sources": sources,
                "processing_time": processing_time
            }
            
        except Exception as e:
            logger.error(f"Error procesando pregunta: {e}")
            return {
                "answer": f"Error procesando la pregunta: {str(e)}",
                "sources": [],
                "processing_time": time.time() - start_time
            }
    
    def _get_fallback_answer(self, question: str, context: str) -> str:
        """Respuesta de fallback cuando GPT4All no está disponible."""
        question_lower = question.lower()
        
        if "requisitos" in question_lower and "facilitador" in question_lower:
            return "Para ser facilitador judicial se requiere: título profesional en áreas afines, experiencia mínima de 3 años, certificación vigente del Consejo Superior de la Judicatura, no tener antecedentes disciplinarios, y renovar certificación cada 3 años."
        elif "duración" in question_lower or "dura" in question_lower:
            return "El procedimiento de conciliación judicial tiene una duración máxima de 30 días hábiles desde la admisión de la solicitud."
        elif "técnicas" in question_lower or "facilitación" in question_lower:
            return "Las técnicas de facilitación incluyen: escucha activa, parafraseo, preguntas abiertas, reformulación y lluvia de ideas."
        elif "costos" in question_lower or "precio" in question_lower:
            return "Los costos incluyen: tasa de admisión $50.000, honorarios del facilitador $100.000 por sesión, y gastos de notificación $25.000 por parte."
        elif "fases" in question_lower or "etapas" in question_lower:
            return "Las fases son: admisión, citación, audiencia y homologación."
        else:
            return "No tengo información suficiente en los documentos provistos para responder a esa pregunta específica."

# Instancia del bot
bot = SimpleBot()

# Inicializar bot
logger.info("🚀 Inicializando bot...")
if bot.load_vector_database():
    bot.load_model()  # Cargar modelo en memoria
    bot.initialized = True
    logger.info("✅ Bot inicializado correctamente")
else:
    logger.error("❌ Error inicializando bot")

# Función de dependencia para autenticación
async def get_current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False))
) -> Optional[Dict[str, Any]]:
    if not ENABLE_AUTH:
        return {
            "user_id": "anonymous",
            "role": "user",
            "created_at": time.time(),
            "expires_at": time.time() + 3600
        }
    
    if not credentials:
        return None
    
    user_info = auth.validate_token(credentials.credentials)
    return user_info

# Eventos de la aplicación
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Inicialización
    logger.info("🚀 Iniciando API de Facilitadores Judiciales...")
    
    if not bot.load_vector_database():
        logger.error("❌ Error inicializando el bot")
        raise Exception("No se pudo inicializar el bot")
    
    bot.initialized = True
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
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoints
@app.get("/")
async def root():
    return {
        "message": "Bot de Facilitadores Judiciales API",
        "version": "1.0.0",
        "status": "active",
        "auth_enabled": ENABLE_AUTH
    }

@app.get("/health")
async def health_check():
    model_available = os.path.exists(MODEL_PATH)
    return {
        "status": "healthy",
        "message": "Sistema funcionando correctamente",
        "model_loaded": model_available,
        "model_path": MODEL_PATH,
        "vector_db_loaded": bot.initialized,
        "documents_count": bot.vectordb._collection.count() if bot.vectordb else 0
    }

@app.post("/ask", response_model=QueryResponse)
async def ask_question(
    request: QueryRequest,
    user_info: Optional[Dict[str, Any]] = Depends(get_current_user)
):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="La pregunta no puede estar vacía")
    
    try:
        user_id = user_info.get("user_id", "anonymous") if user_info else "anonymous"
        logger.info(f"Pregunta de {user_id}: {request.question[:50]}...")
        
        result = bot.ask(request.question)
        
        return QueryResponse(
            answer=result["answer"],
            sources=result["sources"],
            processing_time=result["processing_time"]
        )
        
    except Exception as e:
        logger.error(f"Error en endpoint /ask: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

# Endpoints de autenticación
@app.post("/auth/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    try:
        token = auth.generate_token(request.user_id, request.role)
        logger.info(f"Login exitoso: {request.user_id} ({request.role})")
        
        return LoginResponse(
            access_token=token,
            user_id=request.user_id,
            role=request.role,
            expires_in=86400
        )
        
    except Exception as e:
        logger.error(f"Error en login: {e}")
        raise HTTPException(status_code=500, detail=f"Error generando token: {str(e)}")

@app.get("/auth/me")
async def get_current_user_info(
    user_info: Optional[Dict[str, Any]] = Depends(get_current_user)
):
    if not user_info:
        raise HTTPException(status_code=401, detail="No autenticado")
    
    return {
        "user_id": user_info.get("user_id"),
        "role": user_info.get("role"),
        "permissions": {
            "read": True,
            "write": user_info.get("role") in ["admin", "facilitador"],
            "delete": user_info.get("role") == "admin",
            "manage_users": user_info.get("role") == "admin",
            "view_logs": user_info.get("role") == "admin"
        }
    }

@app.get("/auth/dev-tokens")
async def get_dev_tokens():
    if ENABLE_AUTH:
        raise HTTPException(
            status_code=403,
            detail="Tokens de desarrollo solo disponibles cuando ENABLE_AUTH=false"
        )
    
    return {
        "tokens": auth.dev_tokens,
        "note": "Estos tokens son solo para desarrollo. No usar en producción."
    }

if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("API_HOST", "0.0.0.0")
    
    logger.info(f"🚀 Iniciando servidor en {host}:{port}")
    logger.info(f"🔐 Autenticación: {'Habilitada' if ENABLE_AUTH else 'Deshabilitada'}")
    
    uvicorn.run(
        "api_simple:app",
        host=host,
        port=port,
        reload=True,
        log_level="info"
    )
