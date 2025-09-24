# PASO 3 - Pipeline de recuperación RAG y test en consola

## Objetivo
Crear un chat console que integre la base de datos vectorial con GPT4All para generar respuestas contextuales sobre facilitación judicial.

## Archivos generados
- `chat_console.py` - Script principal del chat con RAG
- `config.env` - Archivo de configuración con variables de entorno
- `README_STEP3.md` - Este archivo de instrucciones

## Características del chat console

### Funcionalidades principales:
- ✅ Integración completa con RAG (Retrieval Augmented Generation)
- ✅ Búsqueda semántica en la base de datos vectorial
- ✅ Respuestas contextuales basadas en documentos
- ✅ Muestra fuentes consultadas
- ✅ Prompt template especializado para facilitadores judiciales
- ✅ Pruebas automáticas con consultas de ejemplo
- ✅ Modo interactivo para preguntas personalizadas

### Prompt template especializado:
El bot está configurado con un prompt específico que:
- Se enfoca en facilitación judicial y resolución de conflictos
- Usa únicamente información de los documentos
- Mantiene un tono profesional y formal
- Menciona fuentes cuando es relevante
- Indica claramente cuando no tiene información suficiente

## Instrucciones de ejecución

### 1. Configurar variables de entorno
```bash
# Opción 1: Usar archivo de configuración
source config.env

# Opción 2: Configurar manualmente
export MODEL_PATH="/ruta/a/tu/modelo.gguf"
export VECTOR_DB_DIR="./data/chroma"
```

### 2. Activar entorno virtual
```bash
source venv/bin/activate
```

### 3. Ejecutar chat console
```bash
python chat_console.py
```

## Salida esperada

El script mostrará:
```
🤖 Bot de Facilitadores Judiciales - Chat Console
============================================================

2024-01-XX XX:XX:XX - INFO - 🚀 Inicializando bot de Facilitadores Judiciales...
2024-01-XX XX:XX:XX - INFO - Cargando base de datos vectorial...
2024-01-XX XX:XX:XX - INFO - ✅ Base de datos cargada con 7 documentos
2024-01-XX XX:XX:XX - INFO - Cargando modelo de lenguaje...
2024-01-XX XX:XX:XX - INFO - ✅ Modelo cargado con LangChain
2024-01-XX XX:XX:XX - INFO - Creando cadena de pregunta-respuesta...
2024-01-XX XX:XX:XX - INFO - ✅ Cadena de QA creada exitosamente
2024-01-XX XX:XX:XX - INFO - ✅ Bot inicializado correctamente

🧪 Ejecutando pruebas automáticas...
============================================================

--- PRUEBA 1 ---
Pregunta: ¿Cuáles son los requisitos para ser facilitador judicial?
Respuesta: [Respuesta basada en los documentos]
Fuentes:
  1. marco_legal.txt
  2. guia_facilitador.txt
--------------------------------------------------

💬 Modo interactivo (escribe 'exit' para salir)
============================================================

🤔 Pregunta: [Tu pregunta aquí]
```

## Pruebas automáticas incluidas

El script ejecuta automáticamente estas consultas de prueba:

1. **"¿Cuáles son los requisitos para ser facilitador judicial?"**
   - Debería devolver información sobre título profesional, experiencia, certificación, etc.

2. **"¿Cuánto dura el procedimiento de conciliación?"**
   - Debería mencionar los 30 días hábiles según el documento

3. **"¿Qué técnicas de facilitación se recomiendan?"**
   - Debería listar escucha activa, parafraseo, preguntas abiertas, etc.

4. **"¿Cuáles son los costos del procedimiento?"**
   - Debería mostrar las tasas y honorarios específicos

## Solución de problemas

### Error: "Modelo no encontrado"
```bash
# Verificar que el modelo existe
ls -la /ruta/a/tu/modelo.gguf

# Actualizar la ruta en config.env
export MODEL_PATH="/ruta/correcta/a/tu/modelo.gguf"
```

### Error: "Base de datos no encontrada"
```bash
# Ejecutar primero la ingesta
python ingest.py
```

### Error: "No module named 'gpt4all'"
```bash
# Reinstalar gpt4all
pip uninstall gpt4all
pip install gpt4all==2.0.0
```

### Error de memoria al cargar el modelo
```bash
# Usar un modelo más pequeño o aumentar la memoria virtual
# En macOS, el sistema maneja esto automáticamente
```

## Comandos útiles

### Verificar configuración
```bash
# Verificar variables de entorno
env | grep -E "(MODEL_PATH|VECTOR_DB_DIR)"

# Verificar que existe la base de datos
ls -la data/chroma/
```

### Probar consultas específicas
```python
# Script de prueba rápida
from chat_console import FacilitadorBot

bot = FacilitadorBot(MODEL_PATH, VECTOR_DB_DIR)
if bot.initialize():
    result = bot.ask("¿Cuáles son las fases del procedimiento?")
    print(result['answer'])
```

## Personalización

### Cambiar el prompt template
Edita la variable `FACILITADOR_PROMPT_TEMPLATE` en `chat_console.py` para:
- Modificar el tono de las respuestas
- Agregar instrucciones específicas
- Cambiar el formato de salida

### Ajustar parámetros de búsqueda
Modifica en `create_qa_chain()`:
```python
retriever = self.vectordb.as_retriever(
    search_kwargs={"k": 5}  # Más documentos para consultar
)
```

### Cambiar configuración del modelo
Modifica en `load_llm()`:
```python
self.llm = GPT4AllLangChain(
    model=self.model_path,
    n_ctx=4096,      # Contexto más grande
    temperature=0.2,  # Más creatividad
    max_tokens=1024   # Respuestas más largas
)
```

## Próximos pasos

Una vez completado este paso:
1. Verifica que las pruebas automáticas funcionan correctamente
2. Prueba el modo interactivo con tus propias preguntas
3. Escribe `continuar` para proceder al **PASO 4** (API backend con FastAPI)

## Notas importantes

- ⚠️ El modelo GPT4All debe estar descargado y en la ruta correcta
- ✅ El sistema usa MPS (Metal Performance Shaders) en macOS para aceleración
- ✅ Las respuestas se basan únicamente en los documentos procesados
- ✅ El sistema muestra las fuentes consultadas para transparencia
