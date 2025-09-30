# 📁 Organización del Proyecto

## ✅ Archivos ESENCIALES (Mantener)

### 🎯 **Archivos Principales de Ejecución**
```
run.py          # ⭐ PRINCIPAL - Inicia sistema completo (API + Web)
start.py        # Inicia solo API
console.py      # Interfaz de consola
test.py         # Tests de integración
status.py       # Verificar estado del sistema
```

### 🧠 **Código del Sistema**
```
api.py          # ⭐ API principal con MockLLM + Groq
app.py          # ⭐ Interfaz web Streamlit (minimalista)
```

### ⚙️ **Configuración**
```
config/
├── config.env  # ⭐ Configuración principal (Groq API Key, etc)
└── security.py # Autenticación y seguridad

requirements.txt # ⭐ Dependencias Python
README.md        # Documentación principal
README_SISTEMA.md # Guía de uso detallada (NUEVO)
```

### 📚 **Datos**
```
data/
├── docs/       # ⭐ Documentos legales (PDFs)
└── chroma/     # Base de datos vectorial (generada automáticamente)

models/         # Modelos LLM locales (opcional, no se usan con Groq)
```

### 🛠️ **Scripts Auxiliares**
```
scripts/
├── ingest.py   # Procesar nuevos documentos
└── setup.sh    # Setup inicial (Linux/Mac)
```

---

## ❌ Archivos ELIMINADOS (Ya no necesarios)

### Archivos de prueba temporales:
- ✅ `check_model.py`
- ✅ `test_conversational.py`
- ✅ `test_deepseek_model.py`
- ✅ `test_groq_system.py`
- ✅ `test_llm_model.py`
- ✅ `test_final.py`
- ✅ `download_mistral.py`
- ✅ `download_mistral_v2.py`
- ✅ `download_phi3.py`
- ✅ `download_model.py`
- ✅ `setup_groq.py`

### Archivos de aplicaciones antiguas (en git status):
- ✅ `app/__init__.py`
- ✅ `app/api.py`
- ✅ `app/security.py`
- ✅ `apps/*` (todas las versiones antiguas)
- ✅ `docs/README_*.md` (documentación vieja)
- ✅ `tests/*` (tests antiguos)

---

## 📊 Estructura Final del Proyecto

```
sistema-facilitadores-judiciales/
│
├── 🎯 EJECUCIÓN
│   ├── run.py              # ⭐ Usar este para iniciar
│   ├── start.py
│   ├── console.py
│   ├── test.py
│   └── status.py
│
├── 🧠 CÓDIGO PRINCIPAL
│   ├── api.py              # ⭐ Backend con MockLLM + Groq
│   └── app.py              # ⭐ Frontend Streamlit
│
├── ⚙️ CONFIGURACIÓN
│   ├── config/
│   │   ├── config.env      # ⭐ Editar aquí Groq API Key
│   │   └── security.py
│   ├── requirements.txt
│   ├── README.md
│   └── README_SISTEMA.md   # Guía completa
│
├── 📚 DATOS
│   ├── data/
│   │   ├── docs/           # PDFs legales
│   │   └── chroma/         # DB vectorial
│   └── models/             # (Opcional, no usado con Groq)
│
└── 🛠️ SCRIPTS
    └── scripts/
        ├── ingest.py       # Procesar documentos
        └── setup.sh

```

---

## 🚀 Cómo usar el proyecto

### 1️⃣ **Iniciar el sistema**
```bash
python run.py
```

### 2️⃣ **Acceder**
- **Interfaz Web**: http://localhost:8501
- **API**: http://localhost:8000
- **Docs**: http://localhost:8000/docs

### 3️⃣ **Configurar Groq** (si aún no lo hiciste)
1. Edita `config/config.env`
2. Agrega tu `GROQ_API_KEY` (gratis en https://console.groq.com)
3. Reinicia: `python run.py`

---

## 🎯 Sistema Híbrido Activo

✅ **MockLLM**: Preguntas comunes (< 1s)  
✅ **Groq API**: Preguntas nuevas (1-3s)  
✅ **ChromaDB**: Búsqueda en documentos legales  
✅ **100% GRATIS**

---

## 📝 Próximos pasos (opcional)

### Agregar más documentos:
1. Coloca PDFs en `data/docs/`
2. Ejecuta: `python scripts/ingest.py`

### Expandir MockLLM:
- Edita `api.py` → clase `PrecomputedResponses`
- Agrega más patrones y respuestas precomputadas

### Cambiar modelo de Groq:
- Edita `config/config.env`
- Cambia `GROQ_MODEL` a:
  - `llama-3.1-8b-instant` (recomendado)
  - `mixtral-8x7b-32768`
  - `gemma2-9b-it`

---

## ✨ El proyecto está LISTO y OPTIMIZADO

**Archivos totales**: ~15 archivos esenciales  
**Archivos eliminados**: ~20 archivos temporales  
**Estado**: ✅ Producción
