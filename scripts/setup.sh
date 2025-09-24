#!/usr/bin/env bash
set -e

echo "🚀 Configurando entorno para Facilitadores Judiciales Bot..."

# Verificar que Python 3.10+ esté instalado
python3 --version

# Crear entorno virtual
echo "📦 Creando entorno virtual..."
python3 -m venv venv

# Activar entorno virtual
echo "🔧 Activando entorno virtual..."
source venv/bin/activate

# Actualizar pip
echo "⬆️ Actualizando pip..."
pip install --upgrade pip

# Instalar dependencias
echo "📚 Instalando dependencias..."
pip install -r requirements.txt

echo "✅ ¡Entorno creado exitosamente!"
echo ""
echo "Para activar el entorno en el futuro, ejecuta:"
echo "source venv/bin/activate"
echo ""
echo "Para desactivar el entorno:"
echo "deactivate"

