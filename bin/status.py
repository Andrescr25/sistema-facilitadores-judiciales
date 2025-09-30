#!/usr/bin/env python3
"""
Sistema de Facilitadores Judiciales - Verificar Estado
"""
import os
import sys
import requests
from pathlib import Path

# Configurar path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

def main():
    """Verifica el estado de todos los servicios."""
    print("🔍 Verificando estado del sistema...")
    print("=" * 50)
    
    # Verificar API
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ API: Funcionando")
            print(f"   • Version: {data.get('version')}")
            print(f"   • Documentos: {data.get('num_documents')}")
            print(f"   • LLM: {data.get('llm_type')}")
            print(f"   • Cache: {data.get('cache_size')} entradas")
        else:
            print("❌ API: Error")
    except requests.exceptions.RequestException:
        print("❌ API: No disponible")
        print("   💡 Ejecuta: python bin/start.py")
    
    print()
    
    # Verificar Streamlit
    try:
        response = requests.get("http://localhost:8501", timeout=5)
        if response.status_code == 200:
            print("✅ Interfaz Web: Funcionando")
            print("   🌐 http://localhost:8501")
        else:
            print("❌ Interfaz Web: Error")
    except requests.exceptions.RequestException:
        print("⚠️  Interfaz Web: No disponible")
        print("   💡 Ejecuta: python inicio.py")
    
    print("=" * 50)

if __name__ == "__main__":
    main()