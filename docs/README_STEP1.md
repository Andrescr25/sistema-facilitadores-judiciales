# PASO 1 - Configuración del Entorno

## Objetivo
Configurar el entorno Python con todas las dependencias necesarias para el bot de Facilitadores Judiciales.

## Archivos generados
- `setup.sh` - Script de configuración automática
- `requirements.txt` - Lista de dependencias con versiones
- `README_STEP1.md` - Este archivo de instrucciones

## Instrucciones de instalación

### 1. Hacer ejecutable el script
```bash
chmod +x setup.sh
```

### 2. Ejecutar configuración automática
```bash
./setup.sh
```

### 3. Verificar instalación
```bash
# Activar entorno virtual
source venv/bin/activate

# Verificar que las librerías se instalaron
python -c "import gpt4all, langchain, chromadb, fastapi, streamlit; print('✅ Todas las dependencias instaladas correctamente')"
```

## Solución de problemas comunes

### Error: "No module named 'gpt4all'"
```bash
# Reinstalar gpt4all con versión específica
pip uninstall gpt4all
pip install gpt4all==2.0.0
```

### Error: "Failed building wheel for chromadb"
```bash
# En macOS, instalar dependencias del sistema
brew install cmake
pip install --upgrade pip setuptools wheel
pip install chromadb
```

### Error: "No module named 'unstructured'"
```bash
# Instalar dependencias adicionales para unstructured
pip install "unstructured[local-inference]"
```

### Error de memoria al instalar
```bash
# Instalar con menos procesos paralelos
pip install -r requirements.txt --no-cache-dir
```

## Verificación del entorno

Después de la instalación, deberías ver:
- Carpeta `venv/` creada
- Todas las librerías importables sin errores
- Mensaje de éxito del script

## Próximos pasos

Una vez completado este paso:
1. Confirma que no hay errores en la instalación
2. Escribe `continuar` para proceder al **PASO 2** (Ingesta de documentos)

## Variables de entorno (para referencia futura)

Estas variables se usarán en los siguientes pasos:
- `MODEL_PATH` - Ruta al modelo GPT4All
- `DATA_DIR` - Carpeta con documentos (./data/docs)
- `VECTOR_DB_DIR` - Base de datos vectorial (./data/chroma)
- `PORT` - Puerto de la API (8000)

