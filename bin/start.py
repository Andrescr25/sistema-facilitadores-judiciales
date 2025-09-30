#!/usr/bin/env python3
"""
Sistema de Facilitadores Judiciales - Iniciar solo API
"""
import os
import sys
import subprocess
from pathlib import Path

# Configurar path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
os.chdir(PROJECT_ROOT)

def main():
    """Inicia solo el servidor API."""
    print("🤖 Bot de Facilitadores Judiciales")
    print("=" * 60)
    print("🚀 Iniciando servidor...")
    print("=" * 60)
    print("✨ Características:")
    print("  • Cache inteligente")
    print("  • Respuestas precomputadas")
    print("  • Procesamiento asíncrono")
    print("  • Respuestas amables y prácticas")
    print("=" * 60)
    print("⏳ Esperando que el servidor esté listo...")
    
    # Iniciar el servidor
    subprocess.run([
        sys.executable, "-m", "uvicorn",
        "src.api:app",
        "--host", "0.0.0.0",
        "--port", "8000"
    ])

if __name__ == "__main__":
    main()