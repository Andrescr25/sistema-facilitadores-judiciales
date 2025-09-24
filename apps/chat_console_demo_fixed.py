#!/usr/bin/env python3
"""
Demo del chat console para el bot de Facilitadores Judiciales.
Versión simplificada que funciona sin modelo GPT4All real.
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
    from langchain.schema import Document
except ImportError as e:
    logger.error(f"Error importando LangChain: {e}")
    logger.error("Ejecuta: pip install langchain langchain-community")
    sys.exit(1)

# Configuración
PERSIST_DIR = os.getenv("VECTOR_DB_DIR", "./data/chroma")
MODEL_EMBED = "all-MiniLM-L6-v2"

class MockLLM:
    """
    Mock del LLM para demostración sin modelo real.
    """
    
    def __init__(self):
        self.name = "Mock LLM (Demo)"
    
    def __call__(self, prompt: str, **kwargs) -> str:
        """
        Simula respuestas del LLM basadas en palabras clave.
        """
        prompt_lower = prompt.lower()
        
        # Respuestas predefinidas basadas en palabras clave
        if "requisitos" in prompt_lower and "facilitador" in prompt_lower:
            return """Para ser facilitador judicial se requiere:
1. Título profesional en derecho, psicología, trabajo social o áreas afines
2. Experiencia mínima de 3 años en resolución de conflictos
3. Certificación vigente del Consejo Superior de la Judicatura
4. No tener antecedentes disciplinarios
5. Renovar certificación cada 3 años

Fuente: marco_legal.txt"""
        
        elif "duración" in prompt_lower or "dura" in prompt_lower:
            return """El procedimiento de conciliación judicial tiene una duración máxima de 30 días hábiles desde la admisión de la solicitud.

El proceso incluye las siguientes fases:
- Fase de admisión
- Fase de citación  
- Fase de audiencia
- Fase de homologación

Fuente: ejemplo_procedimiento.txt"""
        
        elif "técnicas" in prompt_lower or "facilitación" in prompt_lower:
            return """Las técnicas de facilitación recomendadas incluyen:

1. Escucha activa: Prestar atención completa a lo que dicen las partes
2. Parafraseo: Repetir con palabras propias lo expresado
3. Preguntas abiertas: Fomentar la reflexión y el diálogo
4. Reformulación: Ayudar a expresar mejor los intereses
5. Lluvia de ideas: Generar opciones creativas de solución

Fuente: guia_facilitador.txt"""
        
        elif "costos" in prompt_lower or "precio" in prompt_lower:
            return """Los costos del procedimiento de conciliación son:

- Tasa de admisión: $50.000
- Honorarios del facilitador: $100.000 por sesión
- Gastos de notificación: $25.000 por parte

El acuerdo conciliatorio tiene fuerza ejecutiva y es equivalente a una sentencia judicial.

Fuente: ejemplo_procedimiento.txt"""
        
        elif "fases" in prompt_lower or "etapas" in prompt_lower:
            return """Las fases del procedimiento de conciliación son:

1. Fase de admisión: El juez evalúa si la solicitud cumple los requisitos
2. Fase de citación: Se notifica a todas las partes involucradas
3. Fase de audiencia: Se realiza la sesión de conciliación
4. Fase de homologación: Se aprueba el acuerdo alcanzado

Fuente: ejemplo_procedimiento.txt"""
        
        else:
            return """No tengo información suficiente en los documentos provistos para responder a esa pregunta específica. 

Los documentos disponibles contienen información sobre:
- Procedimientos de conciliación judicial
- Requisitos para facilitadores judiciales
- Técnicas de facilitación
- Marco legal aplicable
- Costos y duración de procesos

Por favor, reformula tu pregunta usando términos relacionados con estos temas."""

class FacilitadorBotDemo:
    """
    Bot de demostración para facilitadores judiciales con RAG.
    """
    
    def __init__(self, persist_dir: str):
        self.persist_dir = persist_dir
        self.vectordb = None
        self.llm = MockLLM()
        
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
    
    def search_documents(self, query: str, k: int = 3) -> List[Document]:
        """
        Busca documentos relevantes en la base de datos vectorial.
        """
        if not self.vectordb:
            return []
        
        try:
            results = self.vectordb.similarity_search(query, k=k)
            return results
        except Exception as e:
            logger.error(f"Error buscando documentos: {e}")
            return []
    
    def ask(self, question: str) -> Dict[str, Any]:
        """
        Procesa una pregunta y devuelve la respuesta con fuentes.
        """
        if not self.vectordb:
            return {
                "answer": "Error: Base de datos no cargada",
                "sources": []
            }
        
        try:
            logger.info(f"Procesando pregunta: {question}")
            
            # Buscar documentos relevantes
            relevant_docs = self.search_documents(question, k=3)
            
            # Crear contexto para el LLM
            context = ""
            sources = []
            
            for doc in relevant_docs:
                context += f"\n--- {doc.metadata.get('filename', 'Desconocido')} ---\n"
                context += doc.page_content + "\n"
                
                sources.append({
                    "filename": doc.metadata.get("filename", "Desconocido"),
                    "content": doc.page_content[:200] + "...",
                    "source": doc.metadata.get("source", "Desconocido")
                })
            
            # Crear prompt para el LLM
            prompt = f"""Eres un asistente especializado en facilitación judicial. Responde la pregunta basándote en el contexto proporcionado.

CONTEXTO:
{context}

PREGUNTA: {question}

RESPUESTA:"""
            
            # Generar respuesta
            answer = self.llm(prompt)
            
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
                print("Fuentes consultadas:")
                for j, source in enumerate(result['sources'], 1):
                    print(f"  {j}. {source['filename']}")
            
            print("-" * 50)

def main():
    """
    Función principal del chat console demo.
    """
    print("🤖 Bot de Facilitadores Judiciales - Chat Console (DEMO)")
    print("=" * 70)
    print("⚠️  NOTA: Esta es una versión de demostración que simula el LLM")
    print("   Para usar el modelo real, necesitas descargar un modelo GPT4All")
    print("=" * 70)
    
    # Crear instancia del bot
    bot = FacilitadorBotDemo(PERSIST_DIR)
    
    # Cargar base de datos vectorial
    if not bot.load_vector_database():
        print("❌ Error cargando la base de datos. Revisa los logs.")
        return
    
    # Ejecutar pruebas de ejemplo
    test_queries = [
        "¿Cuáles son los requisitos para ser facilitador judicial?",
        "¿Cuánto dura el procedimiento de conciliación?",
        "¿Qué técnicas de facilitación se recomiendan?",
        "¿Cuáles son los costos del procedimiento?",
        "¿Cuáles son las fases del procedimiento?"
    ]
    
    print("\n🧪 Ejecutando pruebas automáticas...")
    bot.test_retrieval(test_queries)
    
    # Modo interactivo
    print("\n💬 Modo interactivo (escribe 'exit' para salir)")
    print("=" * 70)
    
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
