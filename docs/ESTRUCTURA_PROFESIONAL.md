# 📁 Estructura Profesional del Proyecto

## 🎯 Organización

Este proyecto sigue una estructura profesional estándar para aplicaciones Python empresariales.

## 📂 Directorio Raíz

```
sistema-facilitadores-judiciales/
├── inicio.py                    # 🚀 Script principal de inicio
├── requirements.txt             # 📦 Dependencias del proyecto
├── README.md                    # 📖 Documentación principal
├── .gitignore                   # 🚫 Archivos ignorados por Git
├── .env                         # 🔐 Variables de entorno locales
└── LICENSE                      # 📄 Licencia del proyecto
```

**Archivos en la raíz (solo los esenciales):**
- ✅ `inicio.py` - Script de entrada principal
- ✅ `requirements.txt` - Dependencias estándar Python
- ✅ `README.md` - Documentación visible en GitHub
- ✅ `.gitignore` - Control de versiones
- ✅ `.env` - Variables de entorno (no en git)

## 📁 Carpeta `src/` - Código Fuente

```
src/
├── __init__.py                  # Define el paquete
├── api.py                       # ⚡ Backend principal (FastAPI)
└── app.py                       # 🖥️ Frontend (Streamlit)
```

**Propósito:**
- Contiene **todo el código fuente** del sistema
- Mantiene la raíz limpia
- Facilita imports: `from src.api import JudicialBot`
- Empaquetable como módulo Python

## 📁 Carpeta `bin/` - Scripts Ejecutables

```
bin/
├── __init__.py
├── run.py                       # 🚀 Iniciar sistema completo
├── start.py                     # 🔧 Iniciar solo API
├── console.py                   # 💬 Interfaz de consola
└── status.py                    # 📊 Verificar estado
```

**Propósito:**
- Scripts de **operación y administración**
- Separados del código fuente
- Fáciles de ejecutar: `python bin/start.py`

## 📁 Carpeta `tests/` - Pruebas

```
tests/
├── __init__.py
└── test.py                      # 🧪 Tests de integración
```

**Propósito:**
- **Tests unitarios e integración**
- Separados del código fuente
- Estándar en proyectos Python

## 📁 Carpeta `config/` - Configuración

```
config/
├── config.env                   # ⚙️ Variables de entorno
└── security.py                  # 🔐 Configuración de seguridad
```

**Propósito:**
- **Configuración centralizada**
- API keys y secretos
- Configuración de seguridad

## 📁 Carpeta `data/` - Datos

```
data/
├── docs/                        # 📄 Documentos legales (PDFs)
│   ├── Código Civil.pdf
│   ├── Constitución Política.pdf
│   └── ...
└── chroma/                      # 🗄️ Base de datos vectorial
    ├── chroma.sqlite3
    └── ...
```

**Propósito:**
- **Datos del sistema**
- PDFs y documentos fuente
- Base de datos generada

## 📁 Carpeta `docs/` - Documentación

```
docs/
├── README_SISTEMA.md            # 📖 Guía completa del sistema
├── PROYECTO_ORGANIZADO.md       # 📁 Organización anterior
└── ESTRUCTURA_PROFESIONAL.md    # 📋 Este archivo
```

**Propósito:**
- **Documentación técnica**
- Guías de usuario
- Arquitectura del sistema

## 📁 Carpeta `scripts/` - Scripts Auxiliares

```
scripts/
├── ingest.py                    # 📥 Procesar documentos
└── setup.sh                     # 🔧 Setup inicial (Linux/Mac)
```

**Propósito:**
- **Scripts de mantenimiento**
- Tareas administrativas
- Setup y deployment

## 📁 Carpeta `models/` - Modelos LLM (Opcional)

```
models/
└── Phi-3-mini-4k-instruct-q4.gguf
```

**Propósito:**
- Modelos LLM locales (opcional)
- No usado con Groq API
- Backup offline

## 🎨 Ventajas de esta Estructura

### ✅ **Raíz Limpia**
- Solo archivos esenciales visibles
- Fácil navegación
- Profesional en GitHub

### ✅ **Separación Clara**
- Código fuente (`src/`)
- Scripts operacionales (`bin/`)
- Tests (`tests/`)
- Configuración (`config/`)
- Documentación (`docs/`)

### ✅ **Escalabilidad**
- Fácil agregar nuevos módulos en `src/`
- Nuevos scripts en `bin/`
- Tests organizados

### ✅ **Estándares Python**
- Sigue PEP 8
- Estructura reconocible
- Facilita colaboración

## 🚀 Cómo Usar

### Iniciar Sistema
```bash
# Desde cualquier lugar del proyecto:
python inicio.py

# O directamente:
python bin/run.py
```

### Importar Módulos
```python
# Desde cualquier script:
from src.api import JudicialBot
from src.app import main
```

### Ejecutar Tests
```bash
python tests/test.py
```

### Verificar Estado
```bash
python bin/status.py
```

## 📊 Comparación: Antes vs Después

### ❌ Antes (Desorganizado)
```
raíz/
├── api.py
├── app.py
├── run.py
├── start.py
├── console.py
├── status.py
├── test.py
├── test_groq_system.py
├── test_deepseek.py
├── check_model.py
├── download_mistral.py
├── setup_groq.py
├── README.md
├── README_SISTEMA.md
├── PROYECTO_ORGANIZADO.md
└── ... (17 archivos en raíz)
```

### ✅ Después (Profesional)
```
raíz/
├── inicio.py              # Solo 4 archivos esenciales
├── requirements.txt
├── README.md
├── .gitignore
├── src/                   # Todo el código fuente
├── bin/                   # Scripts ejecutables
├── tests/                 # Tests organizados
├── config/                # Configuración
├── data/                  # Datos
├── docs/                  # Documentación
├── scripts/               # Scripts auxiliares
└── models/                # Modelos (opcional)
```

## 🎯 Resultado

- **17+ archivos** en raíz → **4 archivos** en raíz
- **Organización clara** y profesional
- **Fácil de navegar** y mantener
- **Escalable** para crecimiento futuro
- **Estándar industrial** Python

---

## 📚 Referencias

- [Python Packaging Guide](https://packaging.python.org/)
- [Cookiecutter Data Science](https://drivendata.github.io/cookiecutter-data-science/)
- [Flask Project Structure](https://flask.palletsprojects.com/en/2.3.x/patterns/packages/)
- [Django Project Structure](https://docs.djangoproject.com/en/4.2/intro/tutorial01/)
