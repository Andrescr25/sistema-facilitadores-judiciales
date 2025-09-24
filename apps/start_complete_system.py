#!/usr/bin/env python3
"""
Script para iniciar el sistema completo de Facilitadores Judiciales
con GPT4All, RAG y interfaz web.
"""

import subprocess
import time
import requests
import os
import sys
from pathlib import Path

def check_port(port):
    """Verifica si un puerto está en uso."""
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('localhost', port))
    sock.close()
    return result == 0

def wait_for_api(max_attempts=30):
    """Espera a que la API esté lista."""
    print("⏳ Esperando que la API esté lista...")
    for i in range(max_attempts):
        try:
            response = requests.get("http://localhost:8000/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ API lista - Modelo: {'Cargado' if data.get('model_loaded') else 'No cargado'}")
                print(f"   Base de datos: {data.get('documents_count', 0)} documentos")
                return True
        except:
            pass
        time.sleep(2)
        print(f"   Intento {i+1}/{max_attempts}...")
    return False

def wait_for_streamlit(max_attempts=15):
    """Espera a que Streamlit esté lista."""
    print("⏳ Esperando que Streamlit esté lista...")
    for i in range(max_attempts):
        try:
            response = requests.get("http://localhost:8501", timeout=5)
            if response.status_code == 200:
                print("✅ Streamlit listo")
                return True
        except:
            pass
        time.sleep(2)
        print(f"   Intento {i+1}/{max_attempts}...")
    return False

def main():
    print("=" * 60)
    print("🤖 Bot de Facilitadores Judiciales - Sistema Completo")
    print("=" * 60)
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists("api_simple.py"):
        print("❌ Error: Ejecuta este script desde el directorio del proyecto")
        sys.exit(1)
    
    # Verificar que el modelo existe
    model_path = "/Users/joseandres/Downloads/ChatBot/models/DeepSeek-R1-Distill-Llama-8B-Q4_0.gguf"
    if not os.path.exists(model_path):
        print(f"❌ Error: Modelo no encontrado en {model_path}")
        sys.exit(1)
    
    print(f"✅ Modelo encontrado: {os.path.basename(model_path)}")
    
    # Verificar puertos
    if check_port(8000):
        print("⚠️  Puerto 8000 ya está en uso. Deteniendo procesos...")
        subprocess.run(["pkill", "-f", "python.*api"], capture_output=True)
        time.sleep(2)
    
    if check_port(8501):
        print("⚠️  Puerto 8501 ya está en uso. Deteniendo procesos...")
        subprocess.run(["pkill", "-f", "streamlit"], capture_output=True)
        time.sleep(2)
    
    # Iniciar API
    print("\n🚀 Iniciando API FastAPI...")
    api_process = subprocess.Popen([
        "python", "api_simple.py"
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    if not wait_for_api():
        print("❌ Error: La API no se inició correctamente")
        api_process.terminate()
        sys.exit(1)
    
    # Iniciar Streamlit
    print("\n🌐 Iniciando interfaz Streamlit...")
    streamlit_process = subprocess.Popen([
        "streamlit", "run", "app_streamlit_clean.py", 
        "--server.port", "8501", "--server.headless", "true"
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    if not wait_for_streamlit():
        print("❌ Error: Streamlit no se inició correctamente")
        api_process.terminate()
        streamlit_process.terminate()
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("🎉 ¡Sistema iniciado exitosamente!")
    print("=" * 60)
    print("📡 API Backend: http://localhost:8000")
    print("🌐 Interfaz Web: http://localhost:8501")
    print("📚 Documentación API: http://localhost:8000/docs")
    print("=" * 60)
    print("💡 Instrucciones:")
    print("1. Abre tu navegador en http://localhost:8501")
    print("2. Inicia sesión como 'admin' para acceso completo")
    print("3. Haz preguntas sobre facilitación judicial")
    print("4. El bot usa GPT4All + RAG para respuestas inteligentes")
    print("=" * 60)
    print("⏹️  Presiona Ctrl+C para detener el sistema")
    print("=" * 60)
    
    try:
        # Mantener el script corriendo
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Deteniendo sistema...")
        api_process.terminate()
        streamlit_process.terminate()
        print("✅ Sistema detenido")

if __name__ == "__main__":
    main()
