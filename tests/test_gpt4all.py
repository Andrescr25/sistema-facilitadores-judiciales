#!/usr/bin/env python3
"""
Script de prueba para verificar que GPT4All funciona correctamente.
"""

import os
import sys
from gpt4all import GPT4All

# Configuración
MODEL_PATH = "/Users/joseandres/Downloads/ChatBot/models/DeepSeek-R1-Distill-Llama-8B-Q4_0.gguf"

def test_gpt4all():
    print("🧪 Probando GPT4All...")
    
    # Verificar que el modelo existe
    if not os.path.exists(MODEL_PATH):
        print(f"❌ Modelo no encontrado en: {MODEL_PATH}")
        return False
    
    print(f"✅ Modelo encontrado: {MODEL_PATH}")
    
    try:
        # Cargar modelo
        print("🔄 Cargando modelo...")
        model = GPT4All(MODEL_PATH, device='cpu')
        print("✅ Modelo cargado exitosamente")
        
        # Contexto de prueba
        context = """
        PROCEDIMIENTO DE CONCILIACIÓN JUDICIAL

        1. ADMISIÓN DE LA SOLICITUD
        - Presentación de la solicitud por escrito
        - Verificación de competencia territorial
        - Revisión de requisitos de procedibilidad
        - Término: 5 días hábiles

        2. CITACIÓN A AUDIENCIA
        - Notificación a las partes
        - Fijación de fecha y hora
        - Término: 10 días hábiles para la audiencia
        """
        
        question = "¿Cuáles son los pasos del procedimiento de conciliación?"
        
        # Prompt completo
        prompt = f"""Eres un asistente especializado en facilitación judicial. Responde la pregunta del usuario basándote únicamente en la información proporcionada en el contexto. Si la información no está en el contexto, responde que no tienes información suficiente.

CONTEXTO:
{context}

PREGUNTA: {question}

RESPUESTA:"""
        
        print("🤖 Generando respuesta...")
        print(f"Pregunta: {question}")
        print("-" * 50)
        
        # Generar respuesta
        response = model.generate(prompt, max_tokens=300, temp=0.1)
        
        print("✅ Respuesta generada:")
        print(response)
        print("-" * 50)
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_gpt4all()
    if success:
        print("🎉 ¡Prueba exitosa!")
    else:
        print("💥 Prueba fallida")
        sys.exit(1)
