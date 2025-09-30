# 🤖 Sistema de Facilitadores Judiciales - Costa Rica

Sistema inteligente de asistencia legal con IA híbrida (MockLLM + Groq API) para facilitadores judiciales.

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🚀 Inicio Rápido

```bash
# Instalar dependencias
pip install -r requirements.txt

# Iniciar sistema completo (API + Web)
python inicio.py
```

El sistema estará disponible en:
- **Interfaz Web**: http://localhost:8501
- **API**: http://localhost:8000
- **Documentación API**: http://localhost:8000/docs

## 📋 Requisitos

- Python 3.9 o superior
- 4GB RAM mínimo
- Conexión a Internet (para Groq API)

## ⚙️ Configuración

### 1. API Key de Groq (Recomendado - GRATIS)

1. Crea una cuenta en [console.groq.com](https://console.groq.com)
2. Genera una API Key
3. Edita `config/config.env`:
   ```env
   GROQ_API_KEY=tu_api_key_aqui
   USE_GROQ_API=true
   ```

## 🧠 Sistema Híbrido

El sistema combina **dos tipos de IA**:

| Componente | Velocidad | Uso | Coste |
|------------|-----------|-----|-------|
| **MockLLM** | < 1s | Preguntas comunes | Gratis |
| **Groq API** | 1-3s | Preguntas variadas | Gratis (14,400 req/día) |

## 📁 Estructura del Proyecto

```
sistema-facilitadores-judiciales/
├── src/                    # Código fuente principal
│   ├── api.py             # Backend (FastAPI + IA)
│   ├── app.py             # Frontend (Streamlit)
│   └── __init__.py
├── bin/                    # Scripts de ejecución
│   ├── run.py             # Iniciar sistema completo
│   ├── start.py           # Solo API
│   ├── console.py         # Interfaz consola
│   └── status.py          # Verificar estado
├── tests/                  # Tests
│   └── test.py
├── config/                 # Configuración
│   ├── config.env         # Variables de entorno
│   └── security.py        # Autenticación
├── data/                   # Datos del sistema
│   ├── docs/              # Documentos legales (PDFs)
│   └── chroma/            # Base de datos vectorial
├── scripts/                # Scripts auxiliares
│   └── ingest.py          # Procesar documentos
├── docs/                   # Documentación
│   ├── README_SISTEMA.md
│   └── PROYECTO_ORGANIZADO.md
├── models/                 # Modelos LLM locales (opcional)
├── inicio.py              # 🚀 Script principal
├── requirements.txt       # Dependencias
└── README.md              # Este archivo
```

## 💻 Uso

### Interfaz Web (Recomendado)
```bash
python inicio.py
# Abre http://localhost:8501
```

### API REST
```bash
python bin/start.py

# Probar con curl
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "¿Cómo solicito pensión alimentaria?"}'
```

### Consola
```bash
python bin/console.py
```

### Verificar Estado
```bash
python bin/status.py
```

## 🧪 Tests

```bash
python tests/test.py
```

## 📚 Agregar Documentos Nuevos

```bash
# 1. Coloca tus PDFs en data/docs/
# 2. Ejecuta el script de ingestión:
python scripts/ingest.py
```

## 🎯 Características

✅ **Respuestas instantáneas** para preguntas comunes  
✅ **IA avanzada (Groq)** para preguntas complejas  
✅ **Búsqueda semántica** en documentos legales  
✅ **Historial conversacional** con contexto  
✅ **Cache inteligente** para optimizar rendimiento  
✅ **Interfaz minimalista** tipo ChatGPT  
✅ **100% GRATIS** sin límites de uso razonables

## 🛠️ Tecnologías

- **Backend**: FastAPI, Uvicorn
- **Frontend**: Streamlit
- **IA**: Groq API (Llama 3.1), MockLLM
- **Base de Datos**: ChromaDB (vectorial)
- **Embeddings**: sentence-transformers
- **Docs**: PyPDF, python-docx

## 📖 Documentación Adicional

- [Guía Completa del Sistema](docs/README_SISTEMA.md)
- [Organización del Proyecto](docs/PROYECTO_ORGANIZADO.md)
- [API Documentation](http://localhost:8000/docs) (cuando esté corriendo)

## 🐛 Troubleshooting

### Error: GROQ_API_KEY no configurada
```bash
# Edita config/config.env y agrega tu API Key
nano config/config.env
```

### Error: Módulo no encontrado
```bash
pip install -r requirements.txt
```

### Sistema lento
- Verifica que `USE_GROQ_API=true` en `config/config.env`
- MockLLM debe responder en < 1s
- Groq debe responder en < 3s

## 🤝 Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 👥 Autores

Sistema de Facilitadores Judiciales de Costa Rica

## 📞 Soporte

Para problemas o preguntas:
- Revisa la [documentación](docs/)
- Abre un [issue](https://github.com/tu-usuario/sistema-facilitadores-judiciales/issues)
- Ejecuta `python bin/status.py` para diagnóstico

---

⭐ Si este proyecto te ayudó, dale una estrella en GitHub!