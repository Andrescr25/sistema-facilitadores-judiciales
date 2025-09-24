#!/usr/bin/env python3
"""
Script de prueba para la autenticación y seguridad del bot.
"""

import requests
import json
import time
import sys

def test_authentication():
    """
    Prueba el sistema de autenticación.
    """
    base_url = "http://localhost:8000"
    
    print("🔐 Probando sistema de autenticación...")
    print("=" * 50)
    
    # Test 1: Login y obtención de token
    print("\n1. Probando login...")
    try:
        response = requests.post(f"{base_url}/auth/login?user_id=admin&role=admin")
        if response.status_code == 200:
            data = response.json()
            token = data["access_token"]
            print(f"✅ Login exitoso:")
            print(f"   Token: {token[:20]}...")
            print(f"   Usuario: {data['user_id']}")
            print(f"   Rol: {data['role']}")
            print(f"   Expira en: {data['expires_in']}s")
        else:
            print(f"❌ Error en login: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error en login: {e}")
        return False
    
    # Test 2: Consulta autenticada
    print("\n2. Probando consulta autenticada...")
    try:
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        payload = {"question": "¿Cuáles son los requisitos para ser facilitador judicial?"}
        response = requests.post(f"{base_url}/ask", json=payload, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Consulta exitosa:")
            print(f"   Respuesta: {data['answer'][:100]}...")
            print(f"   Tiempo: {data['processing_time']:.2f}s")
            print(f"   Fuentes: {len(data['sources'])}")
        else:
            print(f"❌ Error en consulta: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Error en consulta: {e}")
    
    # Test 3: Información del usuario
    print("\n3. Probando información del usuario...")
    try:
        response = requests.get(f"{base_url}/auth/me", headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Info del usuario:")
            print(f"   ID: {data['user_id']}")
            print(f"   Rol: {data['role']}")
            print(f"   Permisos: {data['permissions']}")
        else:
            print(f"❌ Error obteniendo info: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Error obteniendo info: {e}")
    
    # Test 4: Estadísticas de seguridad (admin)
    print("\n4. Probando estadísticas de seguridad...")
    try:
        response = requests.get(f"{base_url}/security/stats", headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Estadísticas de seguridad:")
            print(f"   Tokens activos: {data['security_stats']['active_tokens']}")
            print(f"   Requests última hora: {data['security_stats']['total_requests_last_hour']}")
            print(f"   IPs únicas: {data['security_stats']['unique_ips']}")
            print(f"   Auth habilitada: {data['auth_enabled']}")
        else:
            print(f"❌ Error obteniendo stats: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Error obteniendo stats: {e}")
    
    # Test 5: Consulta sin token (debería fallar)
    print("\n5. Probando consulta sin token...")
    try:
        payload = {"question": "¿Cuánto dura el procedimiento?"}
        response = requests.post(f"{base_url}/ask", json=payload)
        
        if response.status_code == 401:
            print("✅ Correctamente rechazada (sin token)")
        else:
            print(f"⚠️  Respuesta inesperada: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Error en test sin token: {e}")
    
    # Test 6: Rate limiting
    print("\n6. Probando rate limiting...")
    try:
        print("   Enviando múltiples requests rápidos...")
        for i in range(5):
            response = requests.post(f"{base_url}/ask", json=payload, headers=headers)
            if response.status_code == 429:
                print(f"✅ Rate limit activado en request {i+1}")
                break
            time.sleep(0.1)
        else:
            print("⚠️  Rate limit no activado (puede ser normal)")
    except Exception as e:
        print(f"❌ Error en rate limiting: {e}")
    
    # Test 7: Logout
    print("\n7. Probando logout...")
    try:
        response = requests.post(f"{base_url}/auth/logout", headers=headers)
        if response.status_code == 200:
            print("✅ Logout exitoso")
        else:
            print(f"❌ Error en logout: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Error en logout: {e}")
    
    print("\n" + "=" * 50)
    print("✅ Pruebas de autenticación completadas")

def test_dev_mode():
    """
    Prueba el modo desarrollo sin autenticación.
    """
    print("\n🧪 Probando modo desarrollo...")
    print("=" * 50)
    
    # Nota: Esto requeriría reiniciar la API con ENABLE_AUTH=false
    print("Para probar modo desarrollo:")
    print("1. Detener la API actual")
    print("2. Ejecutar: export ENABLE_AUTH=false")
    print("3. Reiniciar: python app/api.py")
    print("4. Ejecutar: python test_auth.py --dev")

def main():
    """
    Función principal.
    """
    if len(sys.argv) > 1 and sys.argv[1] == "--dev":
        test_dev_mode()
    else:
        # Esperar un poco para que la API se inicie
        print("⏳ Esperando que la API se inicie...")
        time.sleep(3)
        
        test_authentication()

if __name__ == "__main__":
    main()
