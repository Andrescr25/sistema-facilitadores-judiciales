# 🌐 Interfaz Web del Bot de Facilitadores Judiciales

## Descripción

Interfaz web completa que incluye:
- **Chat interactivo** con el bot de facilitadores judiciales
- **Panel de administración** para gestionar documentos
- **Sistema de autenticación** con roles (admin, facilitador, usuario)
- **Gestión de documentos** en tiempo real

## 🚀 Inicio Rápido

### 1. Iniciar la Aplicación

```bash
# Activar entorno virtual
source venv/bin/activate

# Iniciar aplicación completa (API + Interfaz Web)
python start_web_app.py
```

### 2. Acceder a la Interfaz

- **Interfaz Web**: http://localhost:8501
- **API Backend**: http://localhost:8000
- **Documentación API**: http://localhost:8000/docs

## 👤 Sistema de Autenticación

### Roles Disponibles

| Rol | Permisos | Descripción |
|-----|----------|-------------|
| **admin** | read, write, delete, manage_users, view_logs | Acceso completo al sistema |
| **facilitador** | read, write | Puede hacer preguntas y ver respuestas |
| **user** | read | Solo puede hacer preguntas |

### Iniciar Sesión

1. Abre http://localhost:8501
2. Haz clic en "Iniciar Sesión"
3. Ingresa:
   - **Usuario**: `admin` (para acceso completo)
   - **Rol**: `admin`
4. Haz clic en "Iniciar Sesión"

## 🔧 Panel de Administración

Solo disponible para usuarios con rol `admin`.

### Gestión de Documentos

#### Subir Nuevos Documentos

1. Ve a la pestaña "📁 Gestión de Documentos"
2. Haz clic en "Selecciona archivos para cargar"
3. Selecciona archivos `.txt`, `.pdf`, o `.docx`
4. Haz clic en "💾 Guardar Archivos"
5. Haz clic en "🔄 Procesar Documentos" para indexarlos

#### Ver Documentos Existentes

- Lista de archivos en el directorio `data/docs/`
- Tamaño de cada archivo
- Opción para eliminar archivos

### Estadísticas del Sistema

- Número de documentos indexados
- Mensajes en el chat
- Estado de la API
- Información técnica detallada

### Configuración

- Variables de entorno
- Acciones del sistema
- Limpieza de base de datos

## 💬 Uso del Chat

### Hacer Preguntas

1. Inicia sesión con cualquier rol
2. Escribe tu pregunta en el campo de texto
3. Presiona Enter o haz clic en enviar
4. El bot responderá con información de los documentos

### Preguntas de Ejemplo

- "¿Cuáles son los requisitos para ser facilitador judicial?"
- "¿Cuánto dura el procedimiento de conciliación?"
- "¿Qué técnicas de facilitación se recomiendan?"
- "¿Cuáles son los costos del procedimiento?"

### Ver Fuentes

Cada respuesta incluye:
- **Fuentes consultadas**: Documentos utilizados para la respuesta
- **Tiempo de procesamiento**: Velocidad de la respuesta
- **Contenido relevante**: Fragmentos específicos de los documentos

## 📁 Estructura de Archivos

```
ChatBot/
├── data/
│   ├── docs/           # Documentos originales
│   └── chroma/         # Base de datos vectorial
├── app_streamlit_advanced.py  # Interfaz web avanzada
├── api_simple.py       # API con autenticación
├── start_web_app.py    # Script de inicio
└── README_WEB_INTERFACE.md
```

## 🔧 Configuración Avanzada

### Variables de Entorno

```bash
# En archivo .env o config.env
API_URL=http://localhost:8000
MODEL_PATH=/ruta/a/tu/modelo.gguf
VECTOR_DB_DIR=./data/chroma
DATA_DIR=./data/docs
ENABLE_AUTH=true
```

### Personalización

#### Modificar Roles y Permisos

Edita `api_simple.py` en la función `get_user_permissions()`:

```python
def get_user_permissions(self, role: str) -> Dict[str, bool]:
    permissions = {
        "admin": {
            "read": True,
            "write": True,
            "delete": True,
            "manage_users": True,
            "view_logs": True
        },
        # Agregar nuevos roles aquí
    }
```

#### Personalizar Interfaz

Edita `app_streamlit_advanced.py` para:
- Cambiar colores y estilos
- Agregar nuevas funcionalidades
- Modificar el layout

## 🐛 Solución de Problemas

### La API no responde

```bash
# Verificar que la API esté corriendo
curl http://localhost:8000/health

# Reiniciar la aplicación
pkill -f "python.*api"
python start_web_app.py
```

### Error de autenticación

1. Verifica que `ENABLE_AUTH=true` en la configuración
2. Usa los tokens de desarrollo si es necesario
3. Revisa los logs de la API

### Documentos no se procesan

1. Verifica que los archivos estén en `data/docs/`
2. Ejecuta manualmente: `python ingest.py`
3. Revisa los permisos de archivos

### Interfaz no carga

1. Verifica que Streamlit esté instalado: `pip install streamlit`
2. Verifica el puerto 8501: `lsof -i :8501`
3. Reinicia la aplicación completa

## 📊 Monitoreo

### Logs de la Aplicación

```bash
# Ver logs en tiempo real
tail -f logs/app.log

# Ver logs de la API
curl http://localhost:8000/health | jq
```

### Métricas de Rendimiento

- Tiempo de respuesta promedio
- Número de consultas por minuto
- Uso de memoria y CPU
- Estado de la base de datos vectorial

## 🔒 Seguridad

### Mejores Prácticas

1. **Cambiar tokens por defecto** en producción
2. **Usar HTTPS** en entornos de producción
3. **Configurar rate limiting** apropiado
4. **Monitorear logs** de seguridad
5. **Actualizar dependencias** regularmente

### Configuración de Producción

```bash
# Variables de entorno para producción
SECRET_KEY=tu-clave-secreta-muy-segura
ENABLE_AUTH=true
MAX_REQUESTS_PER_MINUTE=30
TOKEN_EXPIRY_HOURS=8
```

## 📞 Soporte

Para soporte técnico o reportar problemas:

1. Revisa los logs de la aplicación
2. Verifica la configuración
3. Consulta la documentación de la API
4. Contacta al administrador del sistema

---

**¡Disfruta usando el Bot de Facilitadores Judiciales!** 🎉
