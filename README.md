# Sistema de Facilitadores Judiciales

Sistema de chatbot especializado en facilitación judicial con interfaz web y API REST.

## Estructura del Proyecto

```
ChatBot/
├── apps/                    # Aplicaciones principales
│   ├── api_simple.py       # API REST simple
│   ├── app_streamlit*.py   # Interfaces web Streamlit
│   ├── chat_console*.py    # Interfaces de consola
│   └── start_*.py          # Scripts de inicio
├── config/                 # Configuración
│   ├── config.env         # Variables de entorno
│   └── security.py        # Configuración de seguridad
├── data/                   # Datos del sistema
│   ├── docs/              # Documentos fuente
│   └── chroma/            # Base de datos vectorial
├── docs/                   # Documentación
│   └── README_*.md        # Documentación detallada
├── models/                 # Modelos de IA
│   └── *.gguf             # Modelos GGUF
├── scripts/                # Scripts de utilidad
│   ├── ingest.py          # Ingesta de documentos
│   └── setup.sh           # Script de configuración
├── tests/                  # Pruebas
│   ├── test_api.py        # Pruebas de API
│   ├── test_auth.py       # Pruebas de autenticación
│   └── test_gpt4all.py    # Pruebas de modelo
├── app/                    # Módulos de aplicación
│   ├── api.py             # Lógica de API
│   └── security.py        # Seguridad de aplicación
├── requirements.txt        # Dependencias Python
└── venv/                   # Entorno virtual
```

## Inicio Rápido

### 1. Configuración Inicial
```bash
# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp config/config.env.example config/config.env
```

### 2. Ingesta de Documentos
```bash
# Procesar documentos en data/docs/
python scripts/ingest.py
```

### 3. Iniciar Sistema
```bash
# Opción 1: Sistema completo (API + Web)
python apps/start_clean.py

# Opción 2: Solo API
python apps/api_simple.py

# Opción 3: Solo interfaz web
streamlit run apps/app_streamlit_clean.py
```

## Acceso al Sistema

- **Interfaz Web**: http://localhost:8501
- **API Backend**: http://localhost:8000
- **Documentación API**: http://localhost:8000/docs

## Credenciales por Defecto

- **Admin**: admin / admin
- **Facilitador**: facilitador / facilitador  
- **Usuario**: user / user

## Documentación Detallada

Ver carpeta `docs/` para documentación específica:
- `README_STEP1.md` - Configuración inicial
- `README_STEP2.md` - Ingesta de documentos
- `README_STEP3.md` - Configuración de API
- `README_STEP4.md` - Interfaz web
- `README_STEP5.md` - Autenticación
- `README_STEP6.md` - Despliegue
- `README_CLEAN.md` - Versión limpia
- `README_FINAL.md` - Documentación final

## Pruebas

```bash
# Ejecutar todas las pruebas
python -m pytest tests/

# Prueba específica de API
python tests/test_api.py
```

## Desarrollo

### Estructura de Carpetas

- **apps/**: Aplicaciones ejecutables (APIs, interfaces)
- **config/**: Archivos de configuración
- **data/**: Datos del sistema (documentos, vectores)
- **docs/**: Documentación del proyecto
- **models/**: Modelos de IA (GGUF)
- **scripts/**: Scripts de utilidad y automatización
- **tests/**: Pruebas unitarias e integración
- **app/**: Módulos de aplicación (lógica de negocio)

### Convenciones

- Usar rutas absolutas para archivos de configuración
- Mantener separación entre lógica de negocio y presentación
- Documentar cambios en `docs/`
- Ejecutar pruebas antes de commits

