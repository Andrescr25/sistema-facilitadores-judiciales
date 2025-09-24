#!/usr/bin/env python3
"""
Chat console para el bot de Facilitadores Judiciales.
Integra RAG (Retrieval Augmented Generation) con GPT4All local.
"""

import os
import sys
import logging
from typing import List, Dict, Any
from pathlib import Path

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

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

# Configuración
MODEL_PATH = os.getenv("MODEL_PATH", "/Users/joseandres/Downloads/ChatBot/models/deepseek.gguf")
PERSIST_DIR = os.getenv("VECTOR_DB_DIR", "./data/chroma")
MODEL_EMBED = "all-MiniLM-L6-v2"

# Prompt template especializado para facilitadores judiciales
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

class FacilitadorBot:
    """
    Bot especializado en facilitación judicial con RAG.
    """
    
    def __init__(self, model_path: str, persist_dir: str):
        self.model_path = model_path
        self.persist_dir = persist_dir
        self.vectordb = None
        self.qa_chain = None
        self.llm = None
        
    def load_vector_database(self) -> bool:
        """
        Carga la base de datos vectorial existente.
        """
        try:
            logger.info("Cargando base de datos vectorial...")
            
            # Verificar que existe la base de datos
            if not Path(self.persist_dir).exists():
                logger.error(f"Base de datos no encontrada en {self.persist_dir}")
                logger.error("Ejecuta primero: python ingest.py")
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
                logger.error(f"Modelo no encontrado en {self.model_path}")
                logger.error("Descarga un modelo GPT4All y actualiza MODEL_PATH")
                return False
            
            # Intentar cargar con LangChain primero
            try:
                self.llm = GPT4AllLangChain(
                    model=self.model_path,
                    n_ctx=2048,  # Contexto más grande
                    temperature=0.1,  # Respuestas más determinísticas
                    max_tokens=512,  # Respuestas concisas
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
                        logger.error(f"Error con GPT4All nativo: {e2}")
                
                return False
                
        except Exception as e:
            logger.error(f"Error cargando modelo: {e}")
            return False
    
    def create_qa_chain(self) -> bool:
        """
        Crea la cadena de pregunta-respuesta con RAG.
        """
        try:
            logger.info("Creando cadena de pregunta-respuesta...")
            
            if not self.vectordb or not self.llm:
                logger.error("Base de datos o modelo no cargados")
                return False
            
            # Configurar retriever
            retriever = self.vectordb.as_retriever(
                search_kwargs={"k": 3}  # Top 3 documentos más relevantes
            )
            
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
        
        logger.info("✅ Bot inicializado correctamente")
        return True
    
    def ask(self, question: str) -> Dict[str, Any]:
        """
        Procesa una pregunta y devuelve la respuesta con fuentes.
        """
        if not self.qa_chain:
            return {
                "answer": "Error: Bot no inicializado correctamente",
                "sources": []
            }
        
        try:
            logger.info(f"Procesando pregunta: {question}")
            
            # Ejecutar consulta
            result = self.qa_chain({"query": question})
            
            # Extraer respuesta y fuentes
            answer = result.get("result", "No se pudo generar respuesta")
            sources = []
            
            if "source_documents" in result:
                for doc in result["source_documents"]:
                    sources.append({
                        "filename": doc.metadata.get("filename", "Desconocido"),
                        "content": doc.page_content[:200] + "...",
                        "source": doc.metadata.get("source", "Desconocido")
                    })
            
            logger.info(f"Respuesta generada con {len(sources)} fuentes")
            
            return {
                "answer": answer,
                "sources": sources
            }
            
        except Exception as e:
            logger.error(f"Error procesando pregunta: {e}")
            return {
                "answer": f"Error procesando la pregunta: {str(e)}",
                "sources": []
            }
    
    def test_retrieval(self, test_queries: List[str]) -> None:
        """
        Prueba el sistema con consultas de ejemplo.
        """
        logger.info("🧪 Ejecutando pruebas del sistema...")
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n--- PRUEBA {i} ---")
            print(f"Pregunta: {query}")
            
            result = self.ask(query)
            
            print(f"Respuesta: {result['answer']}")
            
            if result['sources']:
                print("Fuentes:")
                for j, source in enumerate(result['sources'], 1):
                    print(f"  {j}. {source['filename']}")
                    print(f"     {source['content']}")
            
            print("-" * 50)

def main():
    """
    Función principal del chat console.
    """
    print("🤖 Bot de Facilitadores Judiciales - Chat Console")
    print("=" * 60)
    
    # Crear instancia del bot
    bot = FacilitadorBot(MODEL_PATH, PERSIST_DIR)
    
    # Inicializar bot
    if not bot.initialize():
        print("❌ Error inicializando el bot. Revisa los logs.")
        return
    
    # Ejecutar pruebas de ejemplo
    test_queries = [
        "¿Cuáles son los requisitos para ser facilitador judicial?",
        "¿Cuánto dura el procedimiento de conciliación?",
        "¿Qué técnicas de facilitación se recomiendan?",
        "¿Cuáles son los costos del procedimiento?"
    ]
    
    print("\n🧪 Ejecutando pruebas automáticas...")
    bot.test_retrieval(test_queries)
    
    # Modo interactivo
    print("\n💬 Modo interactivo (escribe 'exit' para salir)")
    print("=" * 60)
    
    while True:
        try:
            question = input("\n🤔 Pregunta: ").strip()
            
            if question.lower() in ['exit', 'salir', 'quit']:
                print("👋 ¡Hasta luego!")
                break
            
            if not question:
                continue
            
            # Procesar pregunta
            result = bot.ask(question)
            
            # Mostrar respuesta
            print(f"\n🤖 Respuesta: {result['answer']}")
            
            # Mostrar fuentes si las hay
            if result['sources']:
                print("\n📚 Fuentes consultadas:")
                for i, source in enumerate(result['sources'], 1):
                    print(f"  {i}. {source['filename']}")
            
        except KeyboardInterrupt:
            print("\n👋 ¡Hasta luego!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
