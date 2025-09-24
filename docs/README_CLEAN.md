# Sistema de Facilitadores Judiciales

Un asistente inteligente para facilitadores judiciales con interfaz minimalista inspirada en ChatGPT.

## Características

- **Modelo Local**: GPT4All DeepSeek ejecutándose localmente
- **RAG Inteligente**: Búsqueda semántica en documentos especializados
- **Interfaz Minimalista**: Diseño limpio inspirado en ChatGPT
- **Autenticación**: Sistema de roles y permisos
- **Respuestas Contextuales**: Basadas en documentos especializados

## Inicio Rápido

```bash
cd /Users/joseandres/Downloads/ChatBot
source venv/bin/activate
python start_clean.py
```

## Acceso

- **Interfaz Web**: http://localhost:8501
- **API Backend**: http://localhost:8000

## Credenciales

- **Admin**: `admin` / `admin`
- **Facilitador**: `facilitador` / `facilitador`
- **Usuario**: `user` / `user`

## Uso

1. Abre http://localhost:8501
2. Inicia sesión con tus credenciales
3. Escribe tu pregunta en el chat
4. El sistema responderá usando GPT4All + RAG

## Documentos Incluidos

- Requisitos para facilitadores judiciales
- Procedimiento de conciliación judicial
- Técnicas de facilitación
- Marco legal aplicable

## Características de la Interfaz

- **Diseño Limpio**: Sin emojis, estilo minimalista
- **Chat Continuo**: Historial de conversación
- **Fuentes**: Muestra documentos consultados
- **Tiempo de Respuesta**: Indicador de rendimiento
- **Estado del Sistema**: Indicador de conexión

## Requisitos del Sistema

- Python 3.10+
- 8GB RAM mínimo
- macOS o Windows
- Modelo GPT4All (incluido)

## Solución de Problemas

### Reiniciar el Sistema
```bash
pkill -f "python.*api"
pkill -f "streamlit"
python start_clean.py
```

### Verificar Estado
```bash
curl http://localhost:8000/health
curl http://localhost:8501
```

### Problemas de Memoria
- Cierra otras aplicaciones
- Verifica que tienes al menos 8GB RAM disponibles

## Arquitectura

- **Frontend**: Streamlit con CSS personalizado
- **Backend**: FastAPI con autenticación JWT
- **Modelo**: GPT4All DeepSeek (4.4GB)
- **Base de Datos**: ChromaDB para vectores
- **Embeddings**: all-MiniLM-L6-v2

## Seguridad

- **100% Local**: No se envían datos externos
- **Autenticación JWT**: Tokens con expiración
- **Roles Granulares**: Permisos por tipo de usuario
- **Rate Limiting**: Protección contra abuso

---

**Sistema listo para usar con interfaz minimalista y funcionalidad completa.**

