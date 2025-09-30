#!/usr/bin/env python3
"""
Sistema de Facilitadores Judiciales - Costa Rica
Script de inicio principal (sistema completo: API + Interfaz Web)
"""

import subprocess
import sys
import os

# Asegurar que estamos en el directorio correcto
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Ejecutar el script de inicio desde bin/
sys.exit(subprocess.call([sys.executable, "bin/run.py"]))
