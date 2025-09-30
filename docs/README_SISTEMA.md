# Sistema de Facilitadores Judiciales - Costa Rica

## 🚀 Iniciar el Sistema

```bash
python run.py
```

El sistema iniciará:
- **API**: http://localhost:8000
- **Interfaz Web**: http://localhost:8501

## 📁 Estructura del Proyecto

```
sistema-facilitadores-judiciales/
├── api.py                 # API principal (FastAPI)
├── app.py                 # Interfaz web (Streamlit)
├── run.py                 # Iniciar sistema completo
├── start.py               # Solo API
├── console.py             # Interfaz consola
├── test.py                # Tests de integración
├── status.py              # Verificar estado
├── config/
│   ├── config.env         # Configuración principal
│   └── security.py        # Seguridad y autenticación
├── data/
│   ├── docs/              # Documentos legales (PDFs)
│   └── chroma/            # Base de datos vectorial
├── models/                # Modelos LLM locales (opcional)
├── scripts/
│   └── ingest.py          # Procesar documentos
└── requirements.txt       # Dependencias Python
```

## 🧠 Sistema Híbrido

El sistema usa **dos tipos de IA**:

### 1. MockLLM (Instantáneo)
- Preguntas comunes sobre pensión, laboral, facilitadores
- **< 1 segundo** de respuesta
- 100% confiable y verificado

### 2. Groq API (Ultra-rápido)
- Preguntas nuevas/variadas
- **1-3 segundos** de respuesta
- 100% GRATIS (14,400 requests/día)

## ⚙️ Configuración

### Groq API (Recomendado)

1. Ve a: https://console.groq.com
2. Crea una cuenta (gratis)
3. Genera una API Key
4. Edita `config/config.env`:

```env
GROQ_API_KEY=tu_api_key_aqui
USE_GROQ_API=true
GROQ_MODEL=llama-3.1-8b-instant
DISABLE_PRECOMPUTED=false
```

## 📝 Uso

### Interfaz Web
Abre http://localhost:8501 y chatea con el bot

### API Directa
```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "¿Cómo solicito pensión alimentaria?"}'
```

### Consola
```bash
python console.py
```

## 🧪 Tests

```bash
python test.py
```

## 📊 Estado del Sistema

```bash
python status.py
```

## 📚 Agregar Documentos

1. Coloca PDFs en `data/docs/`
2. Ejecuta:
```bash
python scripts/ingest.py
```

## 🔧 Troubleshooting

### Error: GROQ_API_KEY no configurada
- Edita `config/config.env` y agrega tu API key

### Sistema lento
- Verifica que `USE_GROQ_API=true` en config.env
- MockLLM debe responder en < 1s
- Groq debe responder en < 3s

### Error al iniciar
```bash
pip install -r requirements.txt
```

## 📦 Dependencias Principales

- **FastAPI**: API REST
- **Streamlit**: Interfaz web
- **Groq**: LLM en la nube
- **ChromaDB**: Base de datos vectorial
- **LangChain**: Framework de IA

## 🎯 Características

✅ Respuestas instantáneas para preguntas comunes  
✅ LLM para preguntas variadas  
✅ Búsqueda en documentos legales (RAG)  
✅ Historial conversacional  
✅ Cache inteligente  
✅ Interface minimalista tipo ChatGPT  
✅ 100% GRATIS

## 🤝 Soporte

Para problemas o preguntas, revisa los logs en:
- API: stdout del proceso `python run.py`
- Sistema: `logs/system.log` (si existe)

## 📄 Licencia

MIT License - Ver archivo LICENSE
