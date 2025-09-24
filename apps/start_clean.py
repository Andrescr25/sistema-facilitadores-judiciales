#!/usr/bin/env python3
"""
Script para iniciar el sistema con interfaz minimalista
"""

import subprocess
import time
import requests
import os
import sys

def check_port(port):
    """Verifica si un puerto está en uso."""
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('localhost', port))
    sock.close()
    return result == 0

def wait_for_api(max_attempts=30):
    """Espera a que la API esté lista."""
    print("Esperando que la API esté lista...")
    for i in range(max_attempts):
        try:
            response = requests.get("http://localhost:8000/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"API lista - Modelo: {'Cargado' if data.get('model_loaded') else 'No cargado'}")
                print(f"Documentos: {data.get('documents_count', 0)}")
                return True
        except:
            pass
        time.sleep(2)
        print(f"Intento {i+1}/{max_attempts}...")
    return False

def wait_for_streamlit(max_attempts=15):
    """Espera a que Streamlit esté lista."""
    print("Esperando que Streamlit esté lista...")
    for i in range(max_attempts):
        try:
            response = requests.get("http://localhost:8501", timeout=5)
            if response.status_code == 200:
                print("Streamlit listo")
                return True
        except:
            pass
        time.sleep(2)
        print(f"Intento {i+1}/{max_attempts}...")
    return False

def main():
    print("=" * 50)
    print("Sistema de Facilitadores Judiciales")
    print("=" * 50)
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists("apps/api_simple.py"):
        print("Error: Ejecuta este script desde el directorio del proyecto")
        sys.exit(1)
    
    # Verificar que el modelo existe
    model_path = "/Users/joseandres/Downloads/ChatBot/models/DeepSeek-R1-Distill-Llama-8B-Q4_0.gguf"
    if not os.path.exists(model_path):
        print(f"Error: Modelo no encontrado en {model_path}")
        sys.exit(1)
    
    print(f"Modelo encontrado: {os.path.basename(model_path)}")
    
    # Verificar puertos
    if check_port(8000):
        print("Puerto 8000 en uso. Deteniendo procesos...")
        subprocess.run(["pkill", "-f", "python.*api"], capture_output=True)
        time.sleep(2)
    
    if check_port(8501):
        print("Puerto 8501 en uso. Deteniendo procesos...")
        subprocess.run(["pkill", "-f", "streamlit"], capture_output=True)
        time.sleep(2)
    
    # Iniciar API
    print("\nIniciando API...")
    api_process = subprocess.Popen([
        "python", "apps/api_simple.py"
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    if not wait_for_api():
        print("Error: La API no se inició correctamente")
        api_process.terminate()
        sys.exit(1)
    
    # Iniciar Streamlit
    print("\nIniciando interfaz web...")
    streamlit_process = subprocess.Popen([
        "streamlit", "run", "apps/app_streamlit_clean.py", 
        "--server.port", "8501", "--server.headless", "true"
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    if not wait_for_streamlit():
        print("Error: Streamlit no se inició correctamente")
        api_process.terminate()
        streamlit_process.terminate()
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("Sistema iniciado exitosamente")
    print("=" * 50)
    print("Interfaz Web: http://localhost:8501")
    print("API Backend: http://localhost:8000")
    print("=" * 50)
    print("Credenciales:")
    print("- Admin: admin / admin")
    print("- Facilitador: facilitador / facilitador")
    print("- Usuario: user / user")
    print("=" * 50)
    print("Presiona Ctrl+C para detener")
    print("=" * 50)
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nDeteniendo sistema...")
        api_process.terminate()
        streamlit_process.terminate()
        print("Sistema detenido")

if __name__ == "__main__":
    main()
