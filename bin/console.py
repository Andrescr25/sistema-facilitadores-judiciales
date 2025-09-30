#!/usr/bin/env python3
"""
Sistema de Facilitadores Judiciales - Interfaz de Consola
"""
import os
import sys
import requests
from pathlib import Path
from datetime import datetime

# Configurar path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

API_URL = "http://localhost:8000"

def main():
    """Interfaz de consola para chatear con el bot."""
    print("\n" + "=" * 70)
    print("🤖 BOT DE FACILITADORES JUDICIALES - Interfaz de Consola")
    print("=" * 70)
    print("Escriba su pregunta o 'salir' para terminar\n")
    
    # Verificar que la API esté disponible
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        if response.status_code != 200:
            print("❌ Error: La API no está disponible")
            print("💡 Ejecuta: python bin/start.py")
            return
    except requests.exceptions.RequestException:
        print("❌ Error: No se puede conectar con la API")
        print("💡 Ejecuta: python bin/start.py")
        return
    
    print("✅ Conectado al servidor\n")
    
    history = []
    
    while True:
        try:
            # Obtener pregunta del usuario
            question = input("\n🙋 Tú: ").strip()
            
            if not question:
                continue
                
            if question.lower() in ['salir', 'exit', 'quit']:
                print("\n👋 ¡Hasta luego!")
                break
            
            # Enviar pregunta a la API
            print("\n🤖 Bot: ", end="", flush=True)
            
            response = requests.post(
                f"{API_URL}/ask",
                json={"question": question, "history": history},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                answer = data.get("answer", "No se obtuvo respuesta")
                print(answer)
                
                # Actualizar historial
                history.append({"role": "user", "content": question})
                history.append({"role": "assistant", "content": answer})
                
                # Mantener solo últimos 10 mensajes
                if len(history) > 10:
                    history = history[-10:]
            else:
                print(f"❌ Error {response.status_code}: {response.text}")
                
        except KeyboardInterrupt:
            print("\n\n👋 ¡Hasta luego!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()