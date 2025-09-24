# PASO 5 - Interfaz web con Streamlit

## Objetivo
Crear una interfaz web moderna y funcional para el bot de facilitadores judiciales usando Streamlit, proporcionando una experiencia de usuario intuitiva y profesional.

## Archivos generados
- `app_streamlit.py` - Interfaz web principal con Streamlit
- `README_STEP5.md` - Este archivo de instrucciones

## Características de la interfaz

### Diseño moderno:
- ✅ Interfaz de chat intuitiva y responsive
- ✅ Diseño profesional con colores corporativos
- ✅ Sidebar con información del sistema en tiempo real
- ✅ Preguntas de ejemplo para facilitar el uso
- ✅ Indicadores de estado de la API
- ✅ Métricas de documentos cargados

### Funcionalidades implementadas:
- ✅ Chat en tiempo real con el bot
- ✅ Visualización de fuentes consultadas
- ✅ Tiempo de procesamiento de respuestas
- ✅ Historial de conversación persistente
- ✅ Botones de control (limpiar chat, actualizar estado)
- ✅ Preguntas de ejemplo predefinidas
- ✅ Estado del sistema en tiempo real

## Instrucciones de ejecución

### 1. Asegurar que la API esté funcionando
```bash
# En una terminal, iniciar la API
source venv/bin/activate
python app/api.py
```

### 2. En otra terminal, iniciar Streamlit
```bash
# Activar entorno virtual
source venv/bin/activate

# Iniciar interfaz web
streamlit run app_streamlit.py
```

### 3. Acceder a la interfaz
- La interfaz se abrirá automáticamente en: http://localhost:8501
- Si no se abre automáticamente, copia la URL que aparece en la terminal

## Salida esperada

### Al iniciar Streamlit:
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501

  For better performance, consider upgrading to the latest version of Streamlit.
```

### Interfaz web:
- **Header**: Título principal con icono de justicia
- **Sidebar izquierda**: Estado del sistema, documentos, controles
- **Área principal**: Interfaz de chat con mensajes
- **Footer**: Información de la aplicación

## Características de la interfaz

### Sidebar (Panel izquierdo):
- **Estado del sistema**: Indicador visual de conexión con la API
- **Documentos**: Número total y lista de documentos disponibles
- **Controles**: Botones para actualizar estado y limpiar chat
- **Información**: Detalles sobre la aplicación

### Área principal de chat:
- **Mensajes del usuario**: Aparecen a la derecha con fondo azul
- **Respuestas del bot**: Aparecen a la izquierda con fondo morado
- **Fuentes consultadas**: Expandible para ver documentos consultados
- **Tiempo de procesamiento**: Muestra cuánto tardó en responder

### Preguntas de ejemplo:
- 8 preguntas predefinidas para facilitar el uso
- Organizadas en 2 columnas
- Click para enviar automáticamente

## Solución de problemas

### Error: "ModuleNotFoundError: No module named 'streamlit'"
```bash
pip install streamlit
```

### Error: "Connection refused" en la API
```bash
# Verificar que la API esté corriendo
curl http://localhost:8000/health

# Si no está corriendo, iniciarla
python app/api.py
```

### Error: "Address already in use" en Streamlit
```bash
# Cambiar puerto
streamlit run app_streamlit.py --server.port 8502
```

### La interfaz no se actualiza
```bash
# Refrescar la página del navegador
# O usar el botón "Actualizar estado" en la sidebar
```

## Configuración avanzada

### Variables de entorno disponibles:
```bash
API_URL=http://localhost:8000  # URL de la API backend
```

### Personalizar la interfaz:
Edita `app_streamlit.py` y modifica:

**Colores corporativos:**
```python
# En el CSS personalizado
.main-header {
    color: #tu-color-corporativo;
}
```

**Preguntas de ejemplo:**
```python
example_questions = [
    "Tu pregunta personalizada 1",
    "Tu pregunta personalizada 2",
    # ...
]
```

**Configuración de Streamlit:**
```python
st.set_page_config(
    page_title="Tu Título Personalizado",
    page_icon="🏛️",  # Cambiar icono
    layout="wide",    # o "centered"
    initial_sidebar_state="expanded"  # o "collapsed"
)
```

### Configuración de puerto:
```bash
# Cambiar puerto de Streamlit
streamlit run app_streamlit.py --server.port 8502

# Cambiar puerto de la API
export PORT=8001
python app/api.py
```

## Uso de la interfaz

### 1. Hacer una pregunta:
- Escribe en el campo de texto en la parte inferior
- Presiona Enter o haz click en el botón de envío
- Espera la respuesta del bot

### 2. Ver fuentes consultadas:
- Haz click en "📚 Fuentes consultadas" debajo de la respuesta
- Se expandirá mostrando los documentos consultados

### 3. Usar preguntas de ejemplo:
- Haz click en cualquiera de las preguntas predefinidas
- Se enviará automáticamente al bot

### 4. Limpiar el chat:
- Usa el botón "🗑️ Limpiar chat" en la sidebar
- Se borrará todo el historial de conversación

### 5. Actualizar estado:
- Usa el botón "🔄 Actualizar estado" en la sidebar
- Se verificará la conexión con la API y documentos

## Próximos pasos

Una vez completado este paso:
1. Verifica que la interfaz web funciona correctamente
2. Prueba hacer preguntas y ver las respuestas
3. Escribe `continuar` para proceder al **PASO 6** (Autenticación básica y seguridad)

## Notas importantes

- ⚠️ La API debe estar corriendo antes de iniciar Streamlit
- ✅ La interfaz es responsive y funciona en móviles
- ✅ El historial de chat se mantiene durante la sesión
- ✅ Las fuentes consultadas se muestran para transparencia
- ✅ El sistema muestra métricas en tiempo real

## Capturas de pantalla esperadas

### Vista principal:
- Header con título y icono
- Sidebar con estado del sistema
- Área de chat con mensajes
- Campo de entrada en la parte inferior

### Vista de fuentes:
- Respuesta del bot expandida
- Lista de documentos consultados
- Tiempo de procesamiento visible

### Vista de preguntas de ejemplo:
- 8 botones con preguntas predefinidas
- Organizados en 2 columnas
- Fácil acceso para usuarios nuevos
