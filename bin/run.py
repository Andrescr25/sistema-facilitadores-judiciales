#!/usr/bin/env python3
"""
Chat FJ - Servicio Nacional de Facilitadoras y Facilitadores Judiciales
Script de inicio completo (API + Interfaz Web)
"""
import os
import sys
import subprocess
import time
import webbrowser
from pathlib import Path

# Configurar path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
os.chdir(PROJECT_ROOT)

def main():
    """Inicia todo el sistema."""
    print("⚖️  Chat FJ - Facilitadoras y Facilitadores Judiciales")
    print("=" * 50)
    print("🚀 Iniciando sistema completo...")
    
    try:
        # Iniciar API
        print("📡 Iniciando API en puerto 8000...")
        api_process = subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "src.api:app", 
             "--host", "0.0.0.0", "--port", "8000"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )
        
        # Esperar API
        print("⏳ Esperando API...")
        time.sleep(10)
        
        # Iniciar Streamlit
        print("🌐 Iniciando interfaz web en puerto 8501...")
        streamlit_process = subprocess.Popen(
            [sys.executable, "-m", "streamlit", "run", "src/app.py", 
             "--server.port", "8501", "--server.headless", "true"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )
        
        # Esperar Streamlit
        print("⏳ Esperando interfaz web...")
        time.sleep(8)
        
        print("✅ Sistema iniciado correctamente!")
        print("=" * 50)
        print("🌐 Servicios disponibles:")
        print("   • API: http://localhost:8000")
        print("   • Docs: http://localhost:8000/docs")
        print("   • Interfaz Web: http://localhost:8501")
        print("=" * 50)
        print("💡 Para probar:")
        print("   • Abre http://localhost:8501 en tu navegador")
        print("   • O ejecuta: python tests/test.py")
        print("=" * 50)
        
        # Abrir navegador
        print("🌍 Abriendo navegador...")
        webbrowser.open("http://localhost:8501")
        
        print("🛑 Presiona Ctrl+C para detener el sistema")
        
        # Mantener procesos vivos
        api_process.wait()
        streamlit_process.wait()
        
    except KeyboardInterrupt:
        print("\n\n🛑 Deteniendo sistema...")
        api_process.terminate()
        streamlit_process.terminate()
        print("✅ Sistema detenido")

if __name__ == "__main__":
    main()