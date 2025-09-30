#!/usr/bin/env python3
"""
Script para probar la API del bot de Facilitadores Judiciales.
"""

import requests
import json
import time
import sys

def test_api():
    """Prueba la API del bot."""
    base_url = "http://localhost:8000"
    
    # Verificar salud del servidor
    try:
        print("🔍 Verificando servidor...")
        health_response = requests.get(f"{base_url}/health", timeout=5)
        if health_response.status_code == 200:
            health_data = health_response.json()
            print("✅ Servidor funcionando!")
            print(f"   Version: {health_data.get('version')}")
            print(f"   Cache: {health_data.get('cache_stats', {}).get('cache_size', 0)} entradas")
        else:
            print("❌ Servidor no responde correctamente")
            return False
    except Exception as e:
        print(f"❌ No se puede conectar al servidor: {e}")
        print("   Asegúrate de que esté corriendo en http://localhost:8000")
        return False
    
    # Preguntas de prueba
    test_questions = [
        "tengo problemas con mi jefe, mal salario y no tengo vacaciones soy de alajuela que hago, donde voy, donde llamo??",
        "problemas con mi ex esposo porque no me quiere ayudar con el dinero de mi hijo, donde puedo pedir la pension para obligarlo a pagar??",
        "¿Cuáles son los requisitos para ser facilitador judicial?",
        "¿Cuánto dura el procedimiento de conciliación?"
    ]
    
    print("\n" + "="*70)
    print("🧪 PRUEBAS DE VELOCIDAD Y CALIDAD")
    print("="*70)
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n--- PRUEBA {i} ---")
        print(f"Pregunta: {question}")
        
        # Medir tiempo de respuesta
        start_time = time.time()
        
        try:
            response = requests.post(
                f"{base_url}/ask",
                json={"question": question},
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            end_time = time.time()
            total_time = end_time - start_time
            
            if response.status_code == 200:
                data = response.json()
                
                print(f"\n🤖 Respuesta:")
                print(data["answer"])
                
                print(f"\n⏱️ Tiempos:")
                print(f"   • Total (red + procesamiento): {total_time:.3f}s")
                print(f"   • Procesamiento interno: {data.get('processing_time', 0):.3f}s")
                print(f"   • Desde cache: {'✅ Sí' if data.get('cached', False) else '❌ No'}")
                
                if data.get("sources"):
                    print(f"\n📚 Fuentes: {len(data['sources'])} documentos")
                
                # Evaluar calidad de respuesta
                answer = data["answer"].lower()
                if any(word in answer for word in ["donde", "acudir", "teléfono", "horario", "costo"]):
                    print("✅ Respuesta completa y práctica")
                else:
                    print("⚠️ Respuesta podría ser más específica")
                
            else:
                print(f"❌ Error: {response.status_code}")
                print(response.text)
        
        except Exception as e:
            print(f"❌ Error en la prueba: {e}")
        
        print("-" * 50)
    
    # Probar cache (segunda consulta de la misma pregunta)
    print(f"\n--- PRUEBA DE CACHE ---")
    question = test_questions[0]
    print(f"Repitiendo primera pregunta para probar cache...")
    
    start_time = time.time()
    try:
        response = requests.post(
            f"{base_url}/ask",
            json={"question": question},
            timeout=30
        )
        end_time = time.time()
        total_time = end_time - start_time
        
        if response.status_code == 200:
            data = response.json()
            print(f"⏱️ Tiempo con cache: {total_time:.3f}s")
            print(f"✅ Desde cache: {'Sí' if data.get('cached', False) else 'No'}")
        
    except Exception as e:
        print(f"❌ Error probando cache: {e}")
    
    # Obtener estadísticas finales
    try:
        stats_response = requests.get(f"{base_url}/stats", timeout=5)
        if stats_response.status_code == 200:
            stats = stats_response.json()
            print(f"\n📊 ESTADÍSTICAS FINALES:")
            cache_stats = stats.get("cache_stats", {})
            print(f"   • Cache hit rate: {cache_stats.get('hit_rate', '0%')}")
            print(f"   • Respuestas precomputadas: {stats.get('precomputed_responses', 0)}")
            print(f"   • Estado del sistema: {stats.get('system_status', 'unknown')}")
    except:
        pass
    
    print("\n✅ Pruebas completadas!")
    return True

if __name__ == "__main__":
    if not test_api():
        sys.exit(1)
