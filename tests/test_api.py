#!/usr/bin/env python3
"""
Script de prueba para la API de Facilitadores Judiciales.
"""

import requests
import json
import time
import sys

def test_api():
    """
    Prueba los endpoints de la API.
    """
    base_url = "http://localhost:8000"
    
    print("🧪 Probando API de Facilitadores Judiciales...")
    print("=" * 50)
    
    # Test 1: Health check
    print("\n1. Probando endpoint /health...")
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check exitoso:")
            print(f"   Status: {data['status']}")
            print(f"   Modelo cargado: {data['model_loaded']}")
            print(f"   Base de datos: {data['vector_db_loaded']}")
            print(f"   Documentos: {data['documents_count']}")
        else:
            print(f"❌ Health check falló: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error en health check: {e}")
        return False
    
    # Test 2: Root endpoint
    print("\n2. Probando endpoint raíz...")
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Endpoint raíz exitoso: {data['message']}")
        else:
            print(f"❌ Endpoint raíz falló: {response.status_code}")
    except Exception as e:
        print(f"❌ Error en endpoint raíz: {e}")
    
    # Test 3: Ask endpoint
    print("\n3. Probando endpoint /ask...")
    test_questions = [
        "¿Cuáles son los requisitos para ser facilitador judicial?",
        "¿Cuánto dura el procedimiento de conciliación?",
        "¿Qué técnicas de facilitación se recomiendan?"
    ]
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n   Pregunta {i}: {question}")
        try:
            payload = {"question": question}
            response = requests.post(
                f"{base_url}/ask",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Respuesta: {data['answer'][:100]}...")
                print(f"   ⏱️  Tiempo: {data['processing_time']:.2f}s")
                print(f"   📚 Fuentes: {len(data['sources'])}")
            else:
                print(f"   ❌ Error: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    # Test 4: Documents endpoint
    print("\n4. Probando endpoint /documents...")
    try:
        response = requests.get(f"{base_url}/documents", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Info de documentos: {data['total_documents']} documentos")
        else:
            print(f"❌ Error en /documents: {response.status_code}")
    except Exception as e:
        print(f"❌ Error en /documents: {e}")
    
    print("\n" + "=" * 50)
    print("✅ Pruebas completadas")

if __name__ == "__main__":
    # Esperar un poco para que la API se inicie
    print("⏳ Esperando que la API se inicie...")
    time.sleep(3)
    
    test_api()
