# 🤖 Bot de Facilitadores Judiciales - Sistema Completo

Un asistente inteligente para facilitadores judiciales que combina **GPT4All** (modelo local), **RAG** (Recuperación Aumentada por Generación) y una interfaz web moderna.

## ✨ Características

- **🧠 GPT4All Local**: Modelo DeepSeek-R1-Distill-Llama-8B ejecutándose localmente
- **📚 RAG Inteligente**: Búsqueda semántica en documentos especializados
- **🌐 Interfaz Web**: Streamlit con autenticación y roles
- **🔐 Seguridad**: Sistema de autenticación con JWT y control de acceso
- **📊 Panel Admin**: Gestión de documentos y usuarios
- **⚡ Respuestas Rápidas**: Optimizado para consultas sobre facilitación judicial

## 🚀 Inicio Rápido

### Opción 1: Script Automático (Recomendado)
```bash
cd /Users/joseandres/Downloads/ChatBot
source venv/bin/activate
python start_complete_system.py
```

### Opción 2: Manual
```bash
# Terminal 1 - API
cd /Users/joseandres/Downloads/ChatBot
source venv/bin/activate
python api_simple.py

# Terminal 2 - Interfaz Web
cd /Users/joseandres/Downloads/ChatBot
source venv/bin/activate
streamlit run app_streamlit_advanced.py --server.port 8501 --server.headless true
```

## 🌐 Acceso al Sistema

- **Interfaz Web**: http://localhost:8501
- **API Backend**: http://localhost:8000
- **Documentación API**: http://localhost:8000/docs

## 👤 Usuarios y Roles

### Credenciales de Acceso
- **Admin**: `admin` / `admin` - Acceso completo
- **Facilitador**: `facilitador` / `facilitador` - Acceso a consultas
- **Usuario**: `user` / `user` - Acceso básico

### Permisos por Rol
- **Admin**: Consultas + Gestión de documentos + Estadísticas + Gestión de usuarios
- **Facilitador**: Consultas + Subida de documentos
- **Usuario**: Solo consultas

## 📚 Documentos Incluidos

El sistema viene pre-cargado con documentos especializados:

1. **Requisitos para Facilitadores Judiciales**
   - Formación académica requerida
   - Experiencia profesional necesaria
   - Certificaciones y registros
   - Requisitos éticos

2. **Procedimiento de Conciliación Judicial**
   - Admisión de solicitudes
   - Citación a audiencia
   - Etapas del proceso
   - Costos y duración

3. **Técnicas de Facilitación**
   - Escucha activa
   - Comunicación efectiva
   - Gestión de emociones
   - Herramientas específicas

## 🔧 Configuración Técnica

### Modelo GPT4All
- **Archivo**: `DeepSeek-R1-Distill-Llama-8B-Q4_0.gguf`
- **Tamaño**: 4.4 GB
- **Ubicación**: `models/DeepSeek-R1-Distill-Llama-8B-Q4_0.gguf`
- **Dispositivo**: CPU (optimizado para macOS)

### Base de Datos Vectorial
- **Tipo**: ChromaDB
- **Ubicación**: `data/chroma/`
- **Embeddings**: all-MiniLM-L6-v2
- **Documentos**: 13 chunks indexados

### Dependencias Principales
- `gpt4all>=1.0.0` - Modelo de lenguaje local
- `langchain>=0.0.300` - Framework RAG
- `chromadb>=0.3.28` - Base de datos vectorial
- `sentence-transformers>=2.2.2` - Embeddings
- `fastapi>=0.95.0` - API REST
- `streamlit>=1.24.0` - Interfaz web

## 📝 Uso del Sistema

### 1. Iniciar Sesión
1. Abre http://localhost:8501
2. Selecciona tu rol (admin/facilitador/user)
3. Haz clic en "Iniciar Sesión"

### 2. Hacer Consultas
1. Escribe tu pregunta en el chat
2. El bot buscará información relevante en los documentos
3. GPT4All generará una respuesta contextualizada
4. Verás las fuentes consultadas

### 3. Gestión de Documentos (Admin)
1. Inicia sesión como admin
2. Ve al panel de administración
3. Sube nuevos documentos (PDF, DOCX, TXT)
4. Los documentos se procesan automáticamente

## 🔍 Ejemplos de Consultas

### Preguntas Típicas
- "¿Cuáles son los requisitos para ser facilitador judicial?"
- "¿Cuánto dura el procedimiento de conciliación?"
- "¿Qué técnicas de facilitación se recomiendan?"
- "¿Cuáles son los costos del procedimiento?"
- "¿Qué fases tiene la conciliación judicial?"

### Respuestas Inteligentes
El bot combina:
- **Búsqueda semántica** en los documentos
- **Generación contextual** con GPT4All
- **Citas de fuentes** para verificación
- **Respuestas en español** especializadas

## 🛠️ Mantenimiento

### Agregar Nuevos Documentos
1. Coloca archivos en `data/docs/`
2. Ejecuta: `python ingest.py`
3. Los documentos se indexan automáticamente

### Verificar Estado del Sistema
```bash
curl http://localhost:8000/health
```

### Reiniciar el Sistema
```bash
pkill -f "python.*api"
pkill -f "streamlit"
python start_complete_system.py
```

## 📊 Rendimiento

### Tiempos de Respuesta
- **Carga inicial**: ~15 segundos
- **Primera consulta**: ~10-15 segundos (carga del modelo)
- **Consultas posteriores**: ~3-5 segundos
- **Búsqueda vectorial**: <1 segundo

### Recursos del Sistema
- **RAM**: ~6-8 GB (modelo + embeddings)
- **CPU**: Uso moderado durante generación
- **Almacenamiento**: ~5 GB (modelo + datos)

## 🔒 Seguridad

### Autenticación
- Tokens JWT con expiración de 24 horas
- Roles y permisos granulares
- Rate limiting por IP

### Privacidad
- **100% Local**: No se envían datos a servicios externos
- **Modelo Local**: GPT4All ejecuta en tu máquina
- **Datos Privados**: Documentos permanecen en tu sistema

## 🐛 Solución de Problemas

### El modelo no carga
```bash
# Verificar que el archivo existe
ls -la models/DeepSeek-R1-Distill-Llama-8B-Q4_0.gguf

# Verificar permisos
chmod 644 models/DeepSeek-R1-Distill-Llama-8B-Q4_0.gguf
```

### Error de puerto en uso
```bash
# Detener procesos
pkill -f "python.*api"
pkill -f "streamlit"

# Verificar puertos
lsof -i :8000
lsof -i :8501
```

### Problemas de memoria
- Cierra otras aplicaciones
- Reinicia el sistema
- Verifica que tienes al menos 8GB RAM disponibles

## 📞 Soporte

### Logs del Sistema
- **API**: Se muestran en la terminal donde ejecutaste `api_simple.py`
- **Streamlit**: Se muestran en la terminal donde ejecutaste `streamlit`
- **Archivos**: `logs/` (si está configurado)

### Verificación de Estado
```bash
# API
curl http://localhost:8000/health

# Streamlit
curl http://localhost:8501

# Procesos
ps aux | grep -E "(python|streamlit)"
```

## 🎯 Próximas Mejoras

- [ ] Soporte para más formatos de documento
- [ ] Interfaz de gestión de usuarios
- [ ] Exportación de conversaciones
- [ ] Integración con bases de datos externas
- [ ] Modelos adicionales de GPT4All
- [ ] Cache de respuestas frecuentes

---

## 🏆 ¡Sistema Listo!

Tu bot de Facilitadores Judiciales está completamente configurado y funcionando con:

✅ **GPT4All DeepSeek** ejecutándose localmente  
✅ **RAG** con 13 documentos especializados  
✅ **Interfaz web** moderna con autenticación  
✅ **API REST** completa con documentación  
✅ **Sistema de seguridad** con roles y permisos  

**¡Disfruta de tu asistente inteligente para facilitación judicial!** 🎉
