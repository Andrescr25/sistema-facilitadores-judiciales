# PASO 2 - Ingesta de Documentos y Generación de Embeddings

## Objetivo
Procesar documentos PDF, DOCX y TXT, fragmentarlos en chunks y generar embeddings para crear una base de datos vectorial con ChromaDB.

## Archivos generados
- `ingest.py` - Script principal de ingesta
- `data/docs/` - Carpeta con documentos de ejemplo
- `data/chroma/` - Base de datos vectorial (se crea automáticamente)
- `README_STEP2.md` - Este archivo de instrucciones

## Documentos de ejemplo incluidos
- `ejemplo_procedimiento.txt` - Procedimiento de conciliación judicial
- `guia_facilitador.txt` - Guía para facilitadores judiciales
- `marco_legal.txt` - Marco legal de la facilitación judicial

## Instrucciones de ejecución

### 1. Activar entorno virtual
```bash
source venv/bin/activate
```

### 2. Configurar variables de entorno (opcional)
```bash
export DATA_DIR=./data/docs
export VECTOR_DB_DIR=./data/chroma
```

### 3. Ejecutar ingesta de documentos
```bash
python ingest.py
```

### 4. Verificar resultados
```bash
# Verificar que se creó la base de datos
ls -la data/chroma/

# Deberías ver archivos como:
# - chroma.sqlite3
# - index/
# - collection_metadata.json
```

## Salida esperada

El script mostrará logs como:
```
2024-01-XX XX:XX:XX - INFO - 🚀 Iniciando ingesta de documentos para Facilitadores Judiciales
2024-01-XX XX:XX:XX - INFO - Encontrados 3 archivos para procesar
2024-01-XX XX:XX:XX - INFO - Procesando: ejemplo_procedimiento.txt
2024-01-XX XX:XX:XX - INFO - ✅ ejemplo_procedimiento.txt: 1 páginas cargadas
2024-01-XX XX:XX:XX - INFO - Fragmentando documentos...
2024-01-XX XX:XX:XX - INFO - Documentos fragmentados: 15 chunks
2024-01-XX XX:XX:XX - INFO - Generando embeddings...
2024-01-XX XX:XX:XX - INFO - Modelo de embeddings: all-MiniLM-L6-v2
2024-01-XX XX:XX:XX - INFO - ✅ Base de datos vectorial creada con 15 documentos
2024-01-XX XX:XX:XX - INFO - Probando recuperación con consulta: 'procedimiento judicial'
2024-01-XX XX:XX:XX - INFO - Encontrados 3 documentos relevantes:
2024-01-XX XX:XX:XX - INFO - ✅ Ingesta completada exitosamente!
```

## Solución de problemas

### Error: "No module named 'unstructured'"
```bash
pip install "unstructured[local-inference]"
```

### Error: "No module named 'sentence_transformers'"
```bash
pip install sentence-transformers
```

### Error: "ChromaDB not found"
```bash
pip install chromadb
```

### Error de memoria al procesar PDFs grandes
```bash
# Procesar archivos más pequeños o usar un modelo de embeddings más ligero
export MODEL_EMBED="all-MiniLM-L6-v2"
```

## Agregar nuevos documentos

1. Coloca archivos .txt, .pdf o .docx en `data/docs/`
2. Ejecuta `python ingest.py` nuevamente
3. Los nuevos documentos se agregarán a la base de datos existente

## Verificar la base de datos

Puedes verificar que la ingesta funcionó correctamente:

```python
# Script de verificación rápida
from langchain.vectorstores import Chroma
from langchain.embeddings import SentenceTransformerEmbeddings

# Cargar la base de datos
vectordb = Chroma(persist_directory="./data/chroma")

# Contar documentos
print(f"Documentos en la base: {vectordb._collection.count()}")

# Buscar documentos
results = vectordb.similarity_search("conciliación", k=3)
for i, doc in enumerate(results, 1):
    print(f"{i}. {doc.metadata.get('filename')}: {doc.page_content[:100]}...")
```

## Próximos pasos

Una vez completado este paso:
1. Verifica que no hay errores en los logs
2. Confirma que se creó la carpeta `data/chroma/` con archivos
3. Escribe `continuar` para proceder al **PASO 3** (Pipeline de recuperación RAG)

## Configuración avanzada

### Cambiar modelo de embeddings
Edita `ingest.py` y modifica la variable `MODEL_EMBED`:
```python
MODEL_EMBED = "all-mpnet-base-v2"  # Modelo más grande y preciso
# o
MODEL_EMBED = "paraphrase-multilingual-MiniLM-L12-v2"  # Soporte multilingüe
```

### Ajustar tamaño de chunks
Modifica las variables en `ingest.py`:
```python
CHUNK_SIZE = 1500      # Chunks más grandes
CHUNK_OVERLAP = 200    # Más superposición entre chunks
```
