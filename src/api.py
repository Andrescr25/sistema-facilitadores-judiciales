#!/usr/bin/env python3
"""
API optimizada para el bot de Facilitadores Judiciales.
Sistema rápido y eficiente con cache inteligente y respuestas precomputadas.
"""

import os
import sys
import logging
import re
import asyncio
import time
import json
import hashlib
from typing import Dict, Any, List, Optional, AsyncGenerator

# Cargar variables de entorno desde config/config.env
from dotenv import load_dotenv
load_dotenv("config/config.env")
load_dotenv()  # .env si existe (prioridad)
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
from collections import defaultdict, OrderedDict
from pathlib import Path

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Importaciones de FastAPI
try:
    from fastapi import FastAPI, HTTPException, Request, BackgroundTasks
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import StreamingResponse, JSONResponse
    from pydantic import BaseModel
    from contextlib import asynccontextmanager
    import uvicorn
except ImportError as e:
    logger.error(f"Error importando FastAPI: {e}")
    sys.exit(1)

# Importaciones de LangChain
try:
    from langchain_community.vectorstores import Chroma
    from langchain_community.embeddings import SentenceTransformerEmbeddings
    from langchain.schema import Document
except ImportError as e:
    logger.error(f"Error importando LangChain: {e}")
    sys.exit(1)

# Intentar importar llama_cpp para usar el modelo local GGUF
try:
    from llama_cpp import Llama  # type: ignore
    _LLAMA_AVAILABLE = True
except Exception:
    _LLAMA_AVAILABLE = False

# Intentar importar Groq para API en la nube
try:
    from groq import Groq  # type: ignore
    _GROQ_AVAILABLE = True
except Exception:
    _GROQ_AVAILABLE = False

# Configuración
PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIRECTORY", "./data/chroma")
MODEL_PATH = os.getenv("MODEL_PATH", "./models/Phi-3-mini-4k-instruct-q4.gguf")
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
MODEL_EMBED = EMBEDDING_MODEL_NAME
DISABLE_PRECOMPUTED = os.getenv("DISABLE_PRECOMPUTED", "false").lower() == "true"  # Hybrid: MockLLM primero, LLM después
NUM_THREADS = int(os.getenv("NUM_THREADS", "4"))

# Configuración de Groq API
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
USE_GROQ_API = os.getenv("USE_GROQ_API", "true").lower() == "true"
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")


# Modelos de Pydantic para la API
class Message(BaseModel):
    """Mensaje en el historial de conversación."""
    role: str  # 'user' o 'assistant'
    content: str


class QueryRequest(BaseModel):
    """Modelo para peticiones de consulta."""
    question: str
    history: List[Message] = []  # Historial de conversación


class QueryResponse(BaseModel):
    """Modelo para respuestas de consulta."""
    answer: str
    sources: List[Any] = []  # Puede ser string o dict con metadata
    processing_time: float = 0.0
    cached: bool = False


class SmartCache:
    """Cache inteligente con TTL y límite de tamaño."""
    def __init__(self, max_size: int = 1000, ttl: int = 3600):
        self.cache: OrderedDict = OrderedDict()
        self.max_size = max_size
        self.ttl = ttl
        self.hits = 0
        self.misses = 0
        self.lock = threading.Lock()
    
    def get(self, key: str) -> Optional[Dict[str, Any]]:
        """Obtener valor del cache si existe y no ha expirado."""
        with self.lock:
            if key in self.cache:
                value, timestamp = self.cache[key]
                if time.time() - timestamp < self.ttl:
                    self.hits += 1
                    # Mover al final (más reciente)
                    self.cache.move_to_end(key)
                    return value
                else:
                    # Expiró, eliminar
                    del self.cache[key]
            self.misses += 1
            return None
    
    def set(self, key: str, value: Dict[str, Any]) -> None:
        """Guardar valor en cache."""
        with self.lock:
            if key in self.cache:
                self.cache.move_to_end(key)
            self.cache[key] = (value, time.time())
            # Limitar tamaño del cache
            if len(self.cache) > self.max_size:
                self.cache.popitem(last=False)
    
    def clear(self) -> None:
        """Limpiar cache."""
        with self.lock:
            self.cache.clear()
    
    def stats(self) -> Dict[str, Any]:
        """Estadísticas del cache."""
        total = self.hits + self.misses
        hit_rate = (self.hits / total * 100) if total > 0 else 0
        return {
            "size": len(self.cache),
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": f"{hit_rate:.1f}%"
        }


class PrecomputedResponses:
    """Respuestas precomputadas para consultas comunes."""
    def __init__(self):
        self.responses = {
            "pension": {
                "keywords": ["pensión", "alimentos", "manutención", "pago", "hijo", "ex esposo", "ex esposa"],
                "answer": """Entiendo tu situación con la pensión alimentaria. Te explico paso a paso qué hacer:

🏛️ **Dónde ir:**
• Juzgado de Familia de tu circuito judicial
• Defensa Pública (gratuita si calificas económicamente)
• PANI para orientación adicional

📋 **Documentos necesarios:**
• Acta de nacimiento del menor (original y copia)
• Tu cédula de identidad
• Cédula del otro progenitor (si la tienes)
• Comprobantes de gastos del menor
• Tu comprobante de ingresos

🚀 **Qué hacer:**
1. Presenta demanda en el Juzgado de Familia
2. Solicita medidas cautelares si hay urgencia
3. Pide retención salarial automática
4. Si no paga, puede haber apremio corporal

⚡ **Importante:** El incumplimiento puede llevar a retención de salario, embargo de bienes e incluso prisión.

💡 **Consejo:** Lleva todo organizado y pregunta por "medidas provisionales" para pensión urgente.

---

**¿En qué más puedo ayudarte?**
• ¿Necesitás que te explique más sobre alguno de estos pasos?
• ¿Querés saber qué hacer si el padre/madre vive en otro país?
• ¿Te gustaría conocer cuánto tiempo tarda cada etapa del proceso?
• ¿Tenés dudas sobre los costos o si hay manera de hacerlo gratis?

Estoy aquí para ayudarte con lo que necesites. ¡No dudes en preguntar! 😊"""
            },
            "duracion_conciliacion": {
                "keywords": ["cuánto dura", "duración", "tiempo", "demora", "tarda", "cuanto tiempo"],
                "answer": """Una conciliación generalmente dura:

⏱️ **Duración típica:**
• **Primera sesión:** 1-2 horas
• **Proceso completo:** 1-3 sesiones (dependiendo del caso)
• **Plazo total:** Usualmente se resuelve en 1-2 meses

📅 **Factores que influyen:**
• Complejidad del caso
• Disponibilidad de las partes
• Documentación necesaria
• Si hay acuerdo o no

✅ **Ventajas vs juicio:**
• Conciliación: 1-2 meses
• Juicio tradicional: 6 meses a 2+ años

🏛️ **Tipos de conciliación:**
• **Pre-procesal:** Antes de juicio (más rápida)
• **Procesal:** Durante el juicio
• **Judicial:** En el juzgado

💡 **Consejo:** La rapidez depende mucho de la actitud colaborativa de ambas partes.

----

**¿Te puedo ayudar con algo más?**
• ¿Querés saber cómo prepararte para una conciliación?
• ¿Necesitás información sobre qué pasa si no hay acuerdo?
• ¿Te interesa conocer qué casos se pueden conciliar?
• ¿Tenés dudas sobre los requisitos para iniciar?

Estoy aquí para ayudarte. 😊"""
            },
            "facilitador": {
                "keywords": ["facilitador judicial", "ser facilitador", "requisitos facilitador", "trabajo facilitador", "certificación facilitador", "curso facilitador"],
                "answer": """Para ser Facilitador Judicial en Costa Rica, necesitas:

📋 **Requisitos:**
• Ser costarricense o extranjero con residencia legal
• Mayor de 25 años
• Título universitario o experiencia comprobada
• No tener antecedentes penales
• Capacitación certificada por el Poder Judicial

📚 **Capacitación:**
• Curso oficial del Poder Judicial
• Temas: mediación, conciliación, técnicas de facilitación
• Duración: variable según programa

🏛️ **Dónde informarte:**
• Poder Judicial: 2295-3000
• Dirección de Resolución Alterna de Conflictos

💼 **Funciones:**
• Facilitar procesos de conciliación
• Ayudar a las partes a llegar a acuerdos
• Orientar sobre procedimientos

💡 **Consejo:** Contacta directamente al Poder Judicial para información sobre próximas capacitaciones.

---

**¿Algo más en lo que te pueda ayudar?**
• ¿Querés saber más sobre el proceso de capacitación?
• ¿Te interesa conocer las funciones específicas de un facilitador?
• ¿Necesitás información sobre dónde dar el curso?
• ¿Tenés dudas sobre los requisitos o documentos?

Estoy aquí para ayudarte. ¡Seguí preguntando! 📚"""
            },
            "proceso_conciliacion": {
                "keywords": ["cómo funciona conciliación", "proceso de conciliación", "qué es conciliación", "conciliación judicial", "conciliar"],
                "answer": """La conciliación es un proceso voluntario para resolver conflictos. Te explico cómo funciona:

🤝 **¿Qué es?**
Es un proceso donde un facilitador neutral ayuda a las partes a llegar a un acuerdo sin ir a juicio.

📋 **Pasos del proceso:**
1. **Solicitud:** Una o ambas partes piden la conciliación
2. **Citación:** Se notifica a la otra parte
3. **Sesión:** El facilitador modera el diálogo
4. **Acuerdo:** Si hay acuerdo, se firma y tiene validez legal
5. **Sin acuerdo:** Se puede acudir a juicio

✅ **Ventajas:**
• Más rápido que un juicio
• Menos costoso
• Las partes mantienen el control
• Acuerdos más flexibles
• Menos conflictivo

🏛️ **Casos que se pueden conciliar:**
• Pensión alimentaria
• Regulación de visitas
• Conflictos laborales (algunos)
• Asuntos de familia
• Conflictos vecinales

⚠️ **No se concilia:**
• Delitos graves
• Violencia doméstica
• Derechos irrenunciables

💡 **Consejo:** La conciliación funciona mejor cuando ambas partes quieren llegar a un acuerdo.

----

**¿En qué más te puedo ayudar?**
• ¿Necesitás saber dónde solicitar una conciliación?
• ¿Querés conocer qué documentos llevar?
• ¿Te interesa saber cuánto cuesta?
• ¿Tenés dudas sobre si tu caso se puede conciliar?

Preguntame lo que necesites. 😊"""
            }
        }
    
    def find_match(self, question: str) -> Optional[str]:
        """Buscar respuesta precomputada."""
        question_lower = question.lower()
        for category, data in self.responses.items():
            if any(keyword in question_lower for keyword in data["keywords"]):
                return data["answer"]
        return None


class LocalLLM:
    """LLM local basado en llama.cpp para modelos GGUF (CPU/GPU)."""
    def __init__(self, model_path: str, n_ctx: int = 4096, n_threads: int = 4, n_gpu_layers: int = 0):
        self.model_path = model_path
        self.n_ctx = n_ctx
        self.n_threads = n_threads
        self.n_gpu_layers = n_gpu_layers
        self._llama: Optional[Llama] = None

    def _ensure_loaded(self) -> None:
        if self._llama is None:
            self._llama = Llama(
                model_path=self.model_path,
                n_ctx=self.n_ctx,
                n_threads=self.n_threads,
                n_gpu_layers=self.n_gpu_layers,
                verbose=False,
            )

    async def generate_async(self, prompt: str) -> str:
        loop = asyncio.get_event_loop()

        def _run() -> str:
            self._ensure_loaded()
            assert self._llama is not None
            out = self._llama.create_completion(
                prompt=prompt,
                max_tokens=400,  # Reducido para respuestas más rápidas
                temperature=0.7,
                top_p=0.9,
                top_k=40,
                repeat_penalty=1.1,
                stop=["\n\nCONTEXTO:", "\n\nPREGUNTA:", "###", "</s>"]
            )
            return out["choices"][0]["text"].strip()

        return await loop.run_in_executor(None, _run)


# LLM usando Groq API (ultra-rápido y gratuito)
class GroqLLM:
    """LLM usando Groq API en la nube - 1-2 segundos por respuesta."""
    def __init__(self, api_key: str, model: str = "llama-3.1-8b-instant"):
        if not api_key:
            raise ValueError("GROQ_API_KEY no está configurada. Obtén una gratis en: https://console.groq.com")
        self.client = Groq(api_key=api_key)
        self.model = model
        self.name = f"Groq {model}"
    
    async def generate_async(self, prompt: str) -> str:
        """Generación asíncrona ultra-rápida con Groq."""
        loop = asyncio.get_event_loop()
        
        def _run() -> str:
            try:
                completion = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "system",
                            "content": "Sos un facilitador judicial de Costa Rica. Respondé de forma clara, práctica y amable en español."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.7,
                    max_tokens=500,
                    top_p=0.9,
                    stream=False
                )
                return completion.choices[0].message.content.strip()
            except Exception as e:
                logger.error(f"Error en Groq API: {e}")
                return f"Lo siento, hubo un error al procesar tu pregunta. Por favor intenta de nuevo."
        
        return await loop.run_in_executor(None, _run)


# LLM simulado optimizado
class MockLLM:
    def __init__(self):
        self.name = "Optimized Mock LLM"
        self.response_cache = {}
    
    async def generate_async(self, prompt: str) -> str:
        """Generación asíncrona simulada con análisis inteligente."""
        # Simular procesamiento más realista para preguntas complejas
        await asyncio.sleep(0.2)  # 200ms para dar sensación de análisis
        
        prompt_lower = prompt.lower()
        
        # Detectar si es una pregunta compleja que llegó hasta aquí
        if "contexto:" in prompt_lower:
            # Es una pregunta que pasó por RAG, intentar respuesta más inteligente
            return await self._generate_contextual_response(prompt)
        
        # Respuestas para preguntas que no encontraron contexto
        return await self._generate_fallback_response(prompt)
    
    def _add_proactive_followup(self, base_response: str, topic: str) -> str:
        """Agrega seguimiento proactivo al final de la respuesta."""
        followup_templates = {
            "pensión": """

---

**¿En qué más puedo ayudarte?**
• ¿Necesitás que te explique más sobre alguno de estos pasos?
• ¿Querés saber qué hacer si el padre/madre vive en otro país?
• ¿Te gustaría conocer cuánto tiempo tarda cada etapa del proceso?
• ¿Tenés dudas sobre los costos o si hay manera de hacerlo gratis?

Estoy aquí para ayudarte con lo que necesites. ¡No dudes en preguntar! 😊""",
            "laboral": """

---

**¿Te puedo ayudar con algo más?**
• ¿Querés saber qué hacer si te despiden durante este proceso?
• ¿Necesitás información sobre indemnización o liquidación?
• ¿Te gustaría saber cómo presentar una denuncia formal?
• ¿Tenés preguntas sobre tus derechos específicos como trabajador?

Estoy aquí para lo que necesites. ¡Preguntá con confianza! 💪""",
            "facilitador": """

---

**¿Algo más en lo que te pueda ayudar?**
• ¿Querés saber más sobre el proceso de capacitación?
• ¿Te interesa conocer las funciones específicas de un facilitador?
• ¿Necesitás información sobre dónde dar el curso?
• ¿Tenés dudas sobre los requisitos o documentos?

Estoy aquí para ayudarte. ¡Seguí preguntando! 📚""",
            "general": """

---

**¿Necesitás más información?**
• ¿Querés que te aclare algún punto específico?
• ¿Te gustaría saber sobre los costos del procedimiento?
• ¿Necesitás orientación sobre los próximos pasos?
• ¿Tenés otra pregunta relacionada con tu situación?

Con gusto te ayudo con lo que necesites. ¡Preguntá sin pena! 😊"""
        }
        
        # Seleccionar el seguimiento apropiado
        followup = followup_templates.get(topic, followup_templates["general"])
        return base_response + followup
    
    async def _generate_contextual_response(self, prompt: str) -> str:
        """Genera respuesta basada en contexto de documentos."""
        prompt_lower = prompt.lower()
        
        # Analizar el tipo de consulta y extraer ubicación si está presente
        location_mentioned = None
        costa_rica_locations = {
            "san josé": "San José", "cartago": "Cartago", "alajuela": "Alajuela", 
            "heredia": "Heredia", "puntarenas": "Puntarenas", "guanacaste": "Guanacaste",
            "limón": "Limón", "liberia": "Liberia", "pérez zeledón": "Pérez Zeledón",
            "desamparados": "Desamparados", "escazú": "Escazú", "goicoechea": "Goicoechea"
        }
        
        for location, proper_name in costa_rica_locations.items():
            if location in prompt_lower:
                location_mentioned = proper_name
                break
        
        if any(word in prompt_lower for word in ["pensión", "alimentos", "manutención", "hijo", "hija"]):
            if location_mentioned:
                response = f"""Entiendo tu situación con la pensión alimentaria. Como sos de {location_mentioned}, te explico exactamente dónde ir:

🏛️ **Juzgado de Familia de {location_mentioned}**
📍 Ubicado en el Edificio de Tribunales de Justicia de {location_mentioned}
📞 Teléfono: Poder Judicial centralizado 2295-3000 (pedir comunicar con pensiones alimentarias)
⏰ Horario: Lunes a viernes, 8:00 AM - 4:00 PM

🆓 **Defensa Pública (GRATUITA)**
📍 En el mismo edificio de tribunales
💡 Pueden llevarte el caso completo sin costo si calificas económicamente

👶 **PANI - Apoyo adicional (si es para menores)**
📞 Oficina local del PANI en {location_mentioned}
🎯 Te pueden dar orientación legal gratuita y apoyo durante el proceso

📋 **Documentos que DEBES llevar:**
• ✅ Tu cédula de identidad
• ✅ Acta de nacimiento del menor (original y copia)
• ✅ Datos completos del padre/madre (nombre, cédula, dirección, trabajo)
• ✅ Comprobantes de gastos del menor (alimentación, educación, salud, ropa)
• ✅ Tu comprobante de ingresos (si trabajas)
• ✅ Cualquier resolución previa sobre pensión (si existe)

🚀 **Qué podés hacer ahí:**
• Presentar demanda de pensión alimentaria
• Solicitar aumento o rebajo de pensión existente
• Denunciar incumplimiento de pago
• Pedir retención salarial automática
• Solicitar apremio corporal si no paga

⚡ **IMPORTANTE:** Si hay incumplimiento, pueden retener salario, embargar bienes, e incluso ordenar prisión. ¡No esperes más!

💡 **Consejo:** Lleva todo organizado y pregunta por "medidas provisionales" si necesitas pensión urgente mientras se resuelve el caso."""
                return self._add_proactive_followup(response, "pensión")
            else:
                response = """Te entiendo perfectamente, la pensión alimentaria es un derecho fundamental de los menores. Te explico paso a paso:

🎯 **PASO 1: Evalúa tu situación**
• ¿El padre/madre reconoce al menor legalmente?
• ¿Hay acuerdo previo o necesitas demanda judicial?
• ¿Es urgente? (el menor no tiene lo básico)

🏛️ **PASO 2: Dónde ir según tu caso**

**Si hay urgencia extrema:**
• 🚨 Juzgado de Familia - Medidas Cautelares
• 📞 Solicita cita: Poder Judicial (centralizada)
• ⚡ Pueden fijar pensión provisional en días

**Para demanda formal:**
• 📍 Juzgado de Familia de tu circuito judicial
• 🆓 Defensa Pública (gratuita si calificas)
• 💼 Abogado privado (si prefieres)

📋 **PASO 3: Documentos que DEBES llevar**
• ✅ Acta de nacimiento del menor (original y copia)
• ✅ Tu cédula de identidad
• ✅ Cédula del otro progenitor (si la tienes)
• ✅ Comprobantes de gastos del menor:
  - Recibos médicos, medicinas
  - Facturas de alimentación
  - Gastos de educación, ropa
  - Recibo de guardería/cuidado

💰 **PASO 4: Cómo se calcula el monto**
• Ingresos del deudor alimentario
• Necesidades básicas del menor
• Número de hijos que debe mantener
• Capacidad económica de ambos padres

⏰ **PLAZOS IMPORTANTES:**
• No hay plazo para solicitar pensión
• Medidas provisionales: 1-2 semanas
• Proceso completo: 2-6 meses

🆘 **Si no paga la pensión:**
• Apremio corporal (puede ir preso)
• Embargo de salario/bienes
• Retención de licencia de conducir

💡 **CONSEJO:** Lleva todo organizado y no tengas miedo de preguntar en el juzgado. Es tu derecho y el del menor."""
                return self._add_proactive_followup(response, "pensión")
        
        elif any(word in prompt_lower for word in ["laboral", "trabajo", "empleador", "jefe", "salario"]):
            if location_mentioned:
                return f"""Entiendo tu situación laboral. Como sos de {location_mentioned}, te explico exactamente dónde ir:

📋 **PASO 1: Documenta TODO ahora mismo**
• Guarda correos, mensajes, horarios de trabajo
• Anota fechas exactas, horas y testigos
• Fotografía condiciones de trabajo si es necesario
• Conserva todos los recibos de pago

🏢 **Dirección Regional de Trabajo de {location_mentioned}**
📍 Ministerio de Trabajo y Seguridad Social - Oficina {location_mentioned}
📞 Línea gratuita: 800-TRABAJO (800-8722246)
⏰ Horario: Lunes a viernes, 7:00 AM - 4:00 PM
🆓 Servicios completamente GRATUITOS

🚨 **Para casos URGENTES (salarios no pagados):**
• Ve directamente a la oficina sin cita
• Solicita "mediación laboral inmediata"
• Pueden llamar a tu empleador ese mismo día
• Si no resuelve, pasan a inspección formal

⚖️ **Juzgado de Trabajo de {location_mentioned}**
📍 Edificio de Tribunales de Justicia
🎯 Para demandas por despido injustificado
⚡ CRÍTICO: Solo tienes 30 días desde el despido

📄 **Documentos específicos que necesitas:**
• ✅ Tu cédula de identidad
• ✅ Contrato de trabajo (si lo tienes)
• ✅ Últimos 3 recibos de pago
• ✅ Carta de despido o última comunicación del empleador
• ✅ Todas las pruebas del problema (fotos, mensajes, testigos)

💡 **ESTRATEGIA:** Ve primero al Ministerio de Trabajo. Si no resuelven en 15 días, entonces al juzgado. ¡El tiempo corre en tu contra!"""
            else:
                return """Entiendo tu situación laboral. Te guío paso a paso:

📋 **PASO 1: Documenta todo**
• Guarda correos, mensajes, horarios de trabajo
• Anota fechas, horas y testigos de incidentes
• Fotografía condiciones de trabajo si es necesario
• Conserva recibos de pago o comprobantes

🏢 **PASO 2: Dónde acudir según tu problema**

**Para salarios no pagados o atrasos:**
• 📞 Ministerio de Trabajo: 800-TRABAJO (800-8722246)
• 📍 Dirección Regional más cercana
• ⏰ Horario: 7:00 AM - 4:00 PM, lunes a viernes

**Para despidos injustificados:**
• 🏛️ Juzgado de Trabajo de tu zona
• 📄 Presenta demanda dentro de 30 días
• 💼 Considera contratar abogado laboralista

**Para acoso o discriminación:**
• 🚨 Inspección de Trabajo (denuncia inmediata)
• 📞 Línea gratuita: 800-TRABAJO
• 📧 También puedes denunciar en línea

📝 **PASO 3: Qué documentos necesitas**
• Cédula de identidad
• Contrato de trabajo (si lo tienes)
• Últimos 3 recibos de pago
• Certificación laboral o carta de despido
• Pruebas del problema específico

💡 **IMPORTANTE:** No esperes, muchos derechos laborales tienen plazos específicos para reclamar."""
        
        elif any(word in prompt_lower for word in ["facilitador", "conciliación", "mediación"]):
            return """Excelente consulta sobre facilitación judicial:

📚 **Marco normativo:**
• La facilitación judicial está regulada por el Código Procesal Civil
• Requiere certificación del Consejo Superior de la Judicatura
• Es un mecanismo alternativo de resolución de conflictos

🎯 **Proceso típico:**
• Admisión de la solicitud
• Designación del facilitador
• Audiencias de facilitación
• Homologación del acuerdo (si se alcanza)

💡 **Ventajas:** Proceso más rápido, menos formal y con mayor control de las partes sobre el resultado."""
        
        else:
            return """Basándome en la información disponible, te oriento paso a paso:

📋 **PASO 1: Identifica tu situación específica**
• ¿Es un problema civil, laboral, familiar o penal?
• ¿Qué resultado específico buscas obtener?
• ¿Hay urgencia en tu caso?

🏛️ **PASO 2: Instituciones según tu caso**

**Problemas Familiares (pensión, divorcio, custodia):**
📍 Juzgado de Familia de tu circuito
🆓 Defensa Pública disponible
📞 Poder Judicial: 2295-3000

**Problemas Laborales (salarios, despidos):**
📍 Ministerio de Trabajo: 800-TRABAJO (800-8722246)
📍 Juzgados de Trabajo para demandas

**Problemas Civiles (contratos, deudas):**
📍 Juzgados Civiles
💼 Considera abogado especializado

**Violencia o delitos:**
📍 Ministerio Público (Fiscalía)
🚨 OIJ para denuncias: 800-8000645

📄 **PASO 3: Documentos básicos siempre necesarios**
• ✅ Cédula de identidad
• ✅ Documentos relacionados al problema
• ✅ Pruebas (contratos, mensajes, testigos)
• ✅ Comprobantes de gastos si aplica

💡 **IMPORTANTE:** Si no estás seguro, ve primero a la Defensa Pública (gratuita) para orientación inicial. Están en todos los circuitos judiciales."""
    
    async def _generate_fallback_response(self, prompt: str) -> str:
        """Respuesta cuando no hay contexto suficiente."""
        return """Lo siento, necesito más información específica para ayudarte mejor.

🤔 **Para brindarte una respuesta más precisa, podrías:**
• Especificar tu situación particular
• Indicar el tipo de procedimiento que te interesa
• Mencionar si es sobre familia, trabajo, civil, etc.

📚 **Puedo ayudarte con temas como:**
• Pensión alimentaria y derecho de familia
• Problemas laborales y derechos del trabajador
• Facilitación judicial y conciliación
• Procedimientos civiles básicos

¡Reformula tu pregunta con más detalles y te ayudo mejor! 😊"""

# Bot optimizado
class JudicialBot:
    def __init__(self, persist_dir: str):
        self.persist_dir = persist_dir
        self.vectordb = None
        self.llm: Any = MockLLM()
        self.cache = SmartCache()
        self.precomputed = PrecomputedResponses()
        self.executor = ThreadPoolExecutor(max_workers=4)
        self.embedder = None
        # Gate para usar o no precomputadas segun env
        self.use_precomputed: bool = not DISABLE_PRECOMPUTED
        
    async def initialize(self):
        """Inicialización asíncrona."""
        try:
            logger.info("🚀 Inicializando sistema...")
            
            # Cargar embeddings en paralelo
            loop = asyncio.get_event_loop()
            self.embedder = await loop.run_in_executor(
                self.executor, 
                lambda: SentenceTransformerEmbeddings(model_name=MODEL_EMBED)
            )
            
            # Seleccionar modelo de lenguaje (prioridad: Groq API > Local > MockLLM)
            if USE_GROQ_API and _GROQ_AVAILABLE and GROQ_API_KEY:
                try:
                    logger.info(f"🚀 Usando Groq API: {GROQ_MODEL} (ultra-rápido)")
                    self.llm = GroqLLM(api_key=GROQ_API_KEY, model=GROQ_MODEL)
                except Exception as e:
                    logger.warning(f"⚠️ Error configurando Groq: {e}. Usando MockLLM")
                    self.llm = MockLLM()
            elif _LLAMA_AVAILABLE and os.path.exists(MODEL_PATH):
                logger.info(f"🧠 Usando modelo local GGUF: {MODEL_PATH}")
                n_gpu_layers = int(os.getenv("N_GPU_LAYERS", "-1"))
                n_ctx = int(os.getenv("N_CTX", "2048"))
                self.llm = LocalLLM(model_path=MODEL_PATH, n_ctx=n_ctx, n_threads=NUM_THREADS, n_gpu_layers=n_gpu_layers)
            else:
                logger.warning("⚠️ Usando MockLLM de respaldo (configura GROQ_API_KEY para más flexibilidad)")

            # Cargar base de datos vectorial
            if os.path.exists(self.persist_dir):
                self.vectordb = await loop.run_in_executor(
                    self.executor,
                    lambda: Chroma(
                        persist_directory=self.persist_dir,
                        embedding_function=self.embedder
                    )
                )
                
                doc_count = await loop.run_in_executor(
                    self.executor,
                    lambda: self.vectordb._collection.count()
                )
                
                logger.info(f"✅ Sistema inicializado con {doc_count} documentos")
            else:
                logger.warning("⚠️ Base de datos vectorial no encontrada, usando solo respuestas precomputadas")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error en inicialización: {e}")
            return False
    
    async def search_documents_async(self, query: str, k: int = 2) -> List[Document]:
        """Búsqueda asíncrona de documentos."""
        if not self.vectordb:
            return []
        
        try:
            loop = asyncio.get_event_loop()
            results = await loop.run_in_executor(
                self.executor,
                lambda: self.vectordb.similarity_search(query, k=k)
            )
            return results
        except Exception as e:
            logger.error(f"Error en búsqueda: {e}")
            return []
    
    def clean_answer(self, raw_text: str) -> str:
        """Limpia metainstrucciones de la respuesta."""
        if not raw_text:
            return ""
        
        lines = raw_text.splitlines()
        cleaned_lines = []
        
        # Construir patrones prohibidos, respetando ALLOW_CONTACTS
        redact_contacts = os.getenv("ALLOW_CONTACTS", "false").lower() != "true"
        forbidden_patterns = [
            r"^\s*fuente\s*:",
            r"^\s*fuentes\s*:",
            r"^\s*tiempo\s*:",
            r"estructura\s+sugerida",
            r"si no hay provincia",
            r"^\s*contexto\s*:",
            r"^\s*pregunta\s*:",
            r"^\s*respuesta\s*:",
            r"ahora responde",
            r"respuesta estructurada"
        ]
        if redact_contacts:
            forbidden_patterns.append(r"^\s*tel")
        
        forbidden_regexes = [re.compile(pat, re.IGNORECASE) for pat in forbidden_patterns]
        
        for line in lines:
            if any(rx.search(line) for rx in forbidden_regexes):
                continue
            # Evitar placeholders obvios
            if "XXXX" in line:
                continue
            cleaned_lines.append(line)
        
        cleaned = "\n".join(cleaned_lines).strip()
        cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
        
        # Filtrar números telefónicos (según variable de entorno)
        if redact_contacts:
            phone_like = re.compile(r"(?:\+?\d[\d\s().-]{7,}\d)")
            cleaned = phone_like.sub("[consultar directorio oficial]", cleaned)
        
        return cleaned
    
    async def ask_async(self, question: str, history: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Procesamiento asíncrono ultra-rápido de preguntas con contexto conversacional."""
        start_time = time.time()
        if history is None:
            history = []
        
        try:
            # 1. Verificar cache (más rápido)
            cached_response = self.cache.get(question)
            if cached_response:
                cached_response['processing_time'] = time.time() - start_time
                return cached_response
            
            # 2. Verificar respuestas precomputadas (opcional)
            if self.use_precomputed:
                precomputed_answer = self.precomputed.find_match(question)
                if precomputed_answer:
                    response = {
                        "answer": precomputed_answer,
                        "sources": [],
                        "processing_time": time.time() - start_time,
                        "cached": False
                    }
                    # Guardar en cache
                    self.cache.set(question, response)
                    return response
            
            # 3. Procesamiento con RAG (solo si es necesario)
            # Intensificar retrieval para respuestas más ricas
            relevant_docs = await self.search_documents_async(question, k=4)
            
            # Crear contexto limitado
            context = ""
            sources = []
            
            for doc in relevant_docs[:2]:
                filename = doc.metadata.get('filename', 'Documento')
                context += f"\n--- {filename} ---\n"
                context += (doc.page_content[:400] if doc.page_content else "") + "\n"
                
                sources.append({
                    "filename": filename,
                    "content": doc.page_content[:150] + "...",
                    "source": doc.metadata.get("source", "Desconocido")
                })
            
            # Detectar ubicación simple en la pregunta para orientar mejor
            detected_location = None
            for loc in [
                "san josé", "cartago", "alajuela", "heredia", "puntarenas",
                "guanacaste", "limón", "liberia", "pérez zeledón", "desamparados",
                "escazú", "goicoechea"
            ]:
                if loc in question.lower():
                    detected_location = loc.title()
                    break

            location_hint = f"Ubicación detectada: {detected_location}. Adapta la guía a esa localidad, menciona oficinas locales y teléfonos oficiales si se permiten." if detected_location else ""

            # Agregar historial de conversación si existe
            conversation_context = ""
            if history and len(history) > 0:
                conversation_context = "\n\n**CONVERSACIÓN PREVIA:**\n"
                for msg in history[-4:]:  # Solo las últimas 4 interacciones
                    role_label = "Usuario" if msg.get("role") == "user" else "Tú (Facilitador)"
                    conversation_context += f"{role_label}: {msg.get('content', '')}\n"
                conversation_context += "\nConsidera este contexto para dar una respuesta más personalizada y coherente.\n"

            # Crear prompt simplificado para respuestas más rápidas
            prompt = f"""Sos un facilitador judicial de Costa Rica. Respondé de forma clara, práctica y amable en español.

Contexto legal:
{context}

Pregunta: {question}

Respuesta (clara, con pasos si aplica, y al final ofrecé ayuda adicional):"""
            
            # Generar respuesta asíncrona
            answer_raw = await self.llm.generate_async(prompt)
            answer = self.clean_answer(answer_raw)
            
            response = {
                "answer": answer,
                "sources": sources,
                "processing_time": time.time() - start_time,
                "cached": False
            }
            
            # Guardar en cache
            self.cache.set(question, response)
            
            logger.info(f"✅ Respuesta generada en {response['processing_time']:.3f}s")
            return response
            
        except Exception as e:
            logger.error(f"❌ Error procesando pregunta: {e}")
            return {
                "answer": "Disculpa, hubo un error técnico. Por favor intenta de nuevo en un momento.",
                "sources": [],
                "processing_time": time.time() - start_time,
                "cached": False
            }

# Instancia global del bot
bot = JudicialBot(PERSIST_DIR)

# Configuración de la aplicación
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("🚀 Iniciando API...")
    success = await bot.initialize()
    if not success:
        logger.error("❌ Error en inicialización")
    yield
    # Shutdown
    logger.info("👋 Cerrando API...")

app = FastAPI(
    title="Bot de Facilitadores Judiciales",
    description="API optimizada para consultas judiciales con respuestas rápidas y amables",
    version="2.0.0",
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

@app.get("/health")
async def health_check():
    """Verificación de salud del sistema."""
    cache_stats = bot.cache.stats()
    return {
        "status": "healthy",
        "version": "2.0.0",
        "timestamp": datetime.now().isoformat(),
        "cache_stats": cache_stats,
        "features": [
            "Cache inteligente",
            "Respuestas precomputadas", 
            "Procesamiento asíncrono",
            "Operaciones paralelas",
            "Limpieza de respuestas"
        ]
    }

@app.post("/ask", response_model=QueryResponse)
async def ask_question(request: QueryRequest):
    """Endpoint principal para preguntas con respuestas optimizadas."""
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="La pregunta no puede estar vacía")
    
    # Convertir history de Message a dict si es necesario
    history_dicts = [msg.dict() if hasattr(msg, 'dict') else msg for msg in request.history]
    response = await bot.ask_async(request.question, history=history_dicts)
    return QueryResponse(**response)

@app.post("/ask/stream")
async def ask_question_stream(request: QueryRequest):
    """Endpoint con respuesta streaming para percepción de velocidad."""
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="La pregunta no puede estar vacía")
    
    async def generate_stream():
        # Obtener respuesta completa con historial
        history_dicts = [msg.dict() if hasattr(msg, 'dict') else msg for msg in request.history]
        response = await bot.ask_async(request.question, history=history_dicts)
        answer = response["answer"]
        
        # Simular streaming por palabras para percepción de velocidad
        words = answer.split()
        for i, word in enumerate(words):
            chunk = {
                "word": word,
                "is_final": i == len(words) - 1,
                "processing_time": response["processing_time"],
                "cached": response["cached"]
            }
            yield f"data: {json.dumps(chunk, ensure_ascii=False)}\n\n"
            await asyncio.sleep(0.05)  # 50ms entre palabras
        
        # Enviar fuentes al final
        if response["sources"]:
            sources_chunk = {
                "sources": response["sources"],
                "is_sources": True
            }
            yield f"data: {json.dumps(sources_chunk, ensure_ascii=False)}\n\n"
    
    return StreamingResponse(
        generate_stream(),
        media_type="text/plain",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"}
    )

@app.get("/stats")
async def get_stats():
    """Estadísticas del sistema."""
    return {
        "cache_stats": bot.cache.stats(),
        "precomputed_responses": len(bot.precomputed.responses),
        "system_status": "optimal"
    }

@app.get("/documents")
async def get_documents():
    """Obtiene información sobre los documentos cargados."""
    total_docs = 0
    sample_docs = []
    
    try:
        if bot.vectordb:
            # Obtener conteo total de documentos
            collection = bot.vectordb._collection
            total_docs = collection.count()
            
            # Obtener muestra de documentos (primeros 5)
            if total_docs > 0:
                results = collection.get(limit=5)
                if results and 'documents' in results:
                    sample_docs = [
                        {
                            "content": doc[:200] + "..." if len(doc) > 200 else doc,
                            "id": results['ids'][i] if 'ids' in results else str(i)
                        }
                        for i, doc in enumerate(results['documents'])
                    ]
        
        return {
            "total_documents": total_docs,
            "sample_documents": sample_docs,
            "vector_db_status": "active" if bot.vectordb else "inactive"
        }
    except Exception as e:
        logger.error(f"Error obteniendo documentos: {e}")
        return {
            "total_documents": 0,
            "sample_documents": [],
            "vector_db_status": "error",
            "error": str(e)
        }

@app.post("/clear-cache")
async def clear_cache():
    """Limpia el cache del sistema."""
    bot.cache.clear()
    return {"message": "Cache limpiado exitosamente"}

if __name__ == "__main__":
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        workers=1,
        loop="asyncio",
        log_level="info"
    )
