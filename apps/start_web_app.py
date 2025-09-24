#!/usr/bin/env python3
"""
Script para iniciar la aplicación web completa.
Inicia tanto la API como la interfaz Streamlit.
"""

import subprocess
import time
import os
import sys
import signal
import threading
from typing import List

class WebAppManager:
    def __init__(self):
        self.processes: List[subprocess.Popen] = []
        self.running = False
    
    def start_api(self):
        """Inicia la API FastAPI."""
        print("🚀 Iniciando API FastAPI...")
        try:
            # Usar la API simplificada
            process = subprocess.Popen([
                sys.executable, "api_simple.py"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.processes.append(process)
            print("✅ API iniciada en puerto 8000")
            return True
        except Exception as e:
            print(f"❌ Error iniciando API: {e}")
            return False
    
    def start_streamlit(self):
        """Inicia la interfaz Streamlit."""
        print("🌐 Iniciando interfaz Streamlit...")
        try:
            # Usar la interfaz avanzada
            process = subprocess.Popen([
                sys.executable, "-m", "streamlit", "run", 
                "app_streamlit_advanced.py",
                "--server.port", "8501",
                "--server.headless", "true"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.processes.append(process)
            print("✅ Interfaz Streamlit iniciada en puerto 8501")
            return True
        except Exception as e:
            print(f"❌ Error iniciando Streamlit: {e}")
            return False
    
    def wait_for_api(self, timeout=30):
        """Espera a que la API esté disponible."""
        import requests
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                response = requests.get("http://localhost:8000/health", timeout=2)
                if response.status_code == 200:
                    print("✅ API está lista")
                    return True
            except:
                pass
            time.sleep(1)
        
        print("❌ Timeout esperando API")
        return False
    
    def start(self):
        """Inicia toda la aplicación."""
        print("=" * 60)
        print("🤖 Bot de Facilitadores Judiciales - Aplicación Web")
        print("=" * 60)
        
        # Verificar que estamos en el directorio correcto
        if not os.path.exists("api_simple.py"):
            print("❌ Error: No se encuentra api_simple.py")
            print("   Asegúrate de ejecutar este script desde el directorio del proyecto")
            return False
        
        if not os.path.exists("app_streamlit_advanced.py"):
            print("❌ Error: No se encuentra app_streamlit_advanced.py")
            print("   Asegúrate de ejecutar este script desde el directorio del proyecto")
            return False
        
        # Iniciar API
        if not self.start_api():
            return False
        
        # Esperar a que la API esté lista
        if not self.wait_for_api():
            self.stop()
            return False
        
        # Iniciar Streamlit
        if not self.start_streamlit():
            self.stop()
            return False
        
        self.running = True
        
        print("\n" + "=" * 60)
        print("🎉 ¡Aplicación iniciada exitosamente!")
        print("=" * 60)
        print("📡 API Backend: http://localhost:8000")
        print("🌐 Interfaz Web: http://localhost:8501")
        print("📚 Documentación API: http://localhost:8000/docs")
        print("=" * 60)
        print("\n💡 Instrucciones:")
        print("1. Abre tu navegador en http://localhost:8501")
        print("2. Inicia sesión como 'admin' para acceder al panel de administración")
        print("3. Sube documentos en el panel de admin para entrenar el bot")
        print("4. Haz preguntas en el chat")
        print("\n⏹️  Presiona Ctrl+C para detener la aplicación")
        print("=" * 60)
        
        return True
    
    def stop(self):
        """Detiene toda la aplicación."""
        print("\n🛑 Deteniendo aplicación...")
        
        for process in self.processes:
            try:
                process.terminate()
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
            except Exception as e:
                print(f"Error deteniendo proceso: {e}")
        
        self.processes.clear()
        self.running = False
        print("✅ Aplicación detenida")
    
    def run(self):
        """Ejecuta la aplicación hasta que se detenga."""
        if not self.start():
            return
        
        try:
            # Mantener la aplicación corriendo
            while self.running:
                time.sleep(1)
                
                # Verificar que los procesos sigan corriendo
                for process in self.processes:
                    if process.poll() is not None:
                        print(f"❌ Proceso terminado inesperadamente: {process}")
                        self.running = False
                        break
                        
        except KeyboardInterrupt:
            print("\n🛑 Interrupción del usuario")
        finally:
            self.stop()

def main():
    """Función principal."""
    manager = WebAppManager()
    manager.run()

if __name__ == "__main__":
    main()
