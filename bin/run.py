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
    
    api_process = None
    streamlit_process = None
    
    try:
        # Iniciar API (sin capturar output para evitar buffer lleno)
        print("📡 Iniciando API en puerto 8000...")
        api_process = subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "src.api:app", 
             "--host", "0.0.0.0", "--port", "8000"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        
        # Esperar API
        print("⏳ Esperando API...")
        time.sleep(10)
        
        # Iniciar Streamlit (sin capturar output)
        print("🌐 Iniciando interfaz web en puerto 8501...")
        streamlit_process = subprocess.Popen(
            [sys.executable, "-m", "streamlit", "run", "src/app.py", 
             "--server.port", "8501", "--server.headless", "true"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
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
        
        print("🛑 Presiona Ctrl+C para detener el sistema\n")
        
        # Mantener procesos vivos (loop infinito hasta Ctrl+C)
        while True:
            # Verificar si los procesos siguen corriendo
            if api_process.poll() is not None:
                print("❌ API se detuvo inesperadamente")
                break
            if streamlit_process.poll() is not None:
                print("❌ Interfaz web se detuvo inesperadamente")
                break
            time.sleep(1)
        
    except KeyboardInterrupt:
        print("\n\n🛑 Deteniendo sistema...")
    except Exception as e:
        print(f"\n❌ Error: {e}")
    finally:
        # Limpiar procesos
        if api_process:
            api_process.terminate()
            try:
                api_process.wait(timeout=5)
            except:
                api_process.kill()
        
        if streamlit_process:
            streamlit_process.terminate()
            try:
                streamlit_process.wait(timeout=5)
            except:
                streamlit_process.kill()
        
        print("✅ Sistema detenido")

if __name__ == "__main__":
    main()