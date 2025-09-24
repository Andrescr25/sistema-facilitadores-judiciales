# PASO 4 - API Backend con FastAPI

## Objetivo
Crear una API REST que exponga el bot de facilitadores judiciales a través de endpoints HTTP, permitiendo integración con frontends y otros servicios.

## Archivos generados
- `app/api.py` - API principal con FastAPI
- `app/__init__.py` - Paquete de la aplicación
- `README_STEP4.md` - Este archivo de instrucciones

## Características de la API

### Endpoints disponibles:
- **`GET /`** - Información básica de la API
- **`GET /health`** - Estado de salud del sistema
- **`POST /ask`** - Consulta principal al bot
- **`GET /docs`** - Información sobre documentos cargados
- **`GET /docs`** - Documentación automática de la API (Swagger UI)

### Funcionalidades implementadas:
- ✅ CORS configurado para frontend
- ✅ Validación de datos con Pydantic
- ✅ Manejo de errores robusto
- ✅ Logging detallado
- ✅ Modo demo sin modelo real
- ✅ Respuestas con fuentes consultadas
- ✅ Métricas de tiempo de procesamiento

## Instrucciones de ejecución

### 1. Configurar variables de entorno
```bash
# Opción 1: Usar archivo de configuración
source config.env

# Opción 2: Configurar manualmente
export MODEL_PATH="/ruta/a/tu/modelo.gguf"
export VECTOR_DB_DIR="./data/chroma"
export PORT=8000
```

### 2. Activar entorno virtual
```bash
source venv/bin/activate
```

### 3. Ejecutar la API
```bash
# Opción 1: Ejecutar directamente
python app/api.py

# Opción 2: Usar uvicorn
uvicorn app.api:app --host 0.0.0.0 --port 8000 --reload
```

### 4. Verificar que funciona
```bash
# Verificar estado de salud
curl http://localhost:8000/health

# Probar consulta
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "¿Cuáles son los requisitos para ser facilitador judicial?"}'
```

## Salida esperada

### Al iniciar la API:
```
2024-01-XX XX:XX:XX - INFO - 🚀 Iniciando API de Facilitadores Judiciales...
2024-01-XX XX:XX:XX - INFO - Cargando base de datos vectorial...
2024-01-XX XX:XX:XX - INFO - ✅ Base de datos cargada con 7 documentos
2024-01-XX XX:XX:XX - INFO - Cargando modelo de lenguaje...
2024-01-XX XX:XX:XX - INFO - ✅ Modelo cargado con LangChain
2024-01-XX XX:XX:XX - INFO - Creando cadena de pregunta-respuesta...
2024-01-XX XX:XX:XX - INFO - ✅ Cadena de QA creada exitosamente
2024-01-XX XX:XX:XX - INFO - ✅ Bot inicializado correctamente
2024-01-XX XX:XX:XX - INFO - ✅ API lista para recibir requests
2024-01-XX XX:XX:XX - INFO - 🚀 Iniciando servidor en 0.0.0.0:8000
```

### Respuesta del endpoint /health:
```json
{
  "status": "healthy",
  "message": "Sistema funcionando correctamente",
  "model_loaded": true,
  "vector_db_loaded": true,
  "documents_count": 7
}
```

### Respuesta del endpoint /ask:
```json
{
  "answer": "Para ser facilitador judicial se requiere: título profesional en áreas afines, experiencia mínima de 3 años, certificación vigente del Consejo Superior de la Judicatura, no tener antecedentes disciplinarios, y renovar certificación cada 3 años.",
  "sources": [
    {
      "filename": "marco_legal.txt",
      "content": "MARCO LEGAL DE LA FACILITACIÓN JUDICIAL...",
      "source": "./data/docs/marco_legal.txt"
    }
  ],
  "processing_time": 1.23
}
```

## Documentación automática

La API incluye documentación automática disponible en:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Ejemplos de uso

### 1. Consulta básica
```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "¿Cuánto dura el procedimiento de conciliación?"}'
```

### 2. Consulta sobre técnicas
```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "¿Qué técnicas de facilitación se recomiendan?"}'
```

### 3. Consulta sobre costos
```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "¿Cuáles son los costos del procedimiento?"}'
```

### 4. Verificar estado del sistema
```bash
curl http://localhost:8000/health
```

### 5. Obtener información de documentos
```bash
curl http://localhost:8000/docs
```

## Solución de problemas

### Error: "ModuleNotFoundError: No module named 'fastapi'"
```bash
pip install fastapi uvicorn
```

### Error: "Bot no inicializado"
```bash
# Verificar que la base de datos existe
ls -la data/chroma/

# Si no existe, ejecutar ingesta
python ingest.py
```

### Error: "Modelo no encontrado"
```bash
# La API funciona en modo demo sin modelo real
# Para usar modelo real, descarga uno y actualiza MODEL_PATH
```

### Error de puerto en uso
```bash
# Cambiar puerto
export PORT=8001
uvicorn app.api:app --port 8001
```

## Configuración avanzada

### Variables de entorno disponibles:
```bash
MODEL_PATH=/ruta/a/tu/modelo.gguf    # Ruta al modelo GPT4All
VECTOR_DB_DIR=./data/chroma          # Base de datos vectorial
PORT=8000                            # Puerto de la API
API_HOST=0.0.0.0                     # Host de la API
```

### Configuración de CORS para producción:
Edita `app/api.py` y modifica:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://tu-dominio.com"],  # Solo tu dominio
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

### Configuración de logging:
```python
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('api.log'),
        logging.StreamHandler()
    ]
)
```

## Próximos pasos

Una vez completado este paso:
1. Verifica que la API responde correctamente
2. Prueba los endpoints con curl o Postman
3. Escribe `continuar` para proceder al **PASO 5** (Interfaz web con Streamlit)

## Notas importantes

- ⚠️ La API funciona en modo demo sin modelo GPT4All real
- ✅ CORS está configurado para permitir requests desde cualquier origen
- ✅ La API incluye documentación automática en `/docs`
- ✅ El sistema maneja errores graciosamente
- ✅ Las respuestas incluyen tiempo de procesamiento para métricas
