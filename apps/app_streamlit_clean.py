import streamlit as st
import requests
import os
import json
import time

# Configuración
API_URL = os.getenv("API_URL", "http://localhost:8000")
ASK_ENDPOINT = f"{API_URL}/ask"
HEALTH_ENDPOINT = f"{API_URL}/health"
LOGIN_ENDPOINT = f"{API_URL}/auth/login"
ME_ENDPOINT = f"{API_URL}/auth/me"

# Configuración de la página
st.set_page_config(
    page_title="Facilitadores Judiciales",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado para estilo minimalista
st.markdown("""
<style>
    .main-header {
        font-size: 2rem;
        font-weight: 600;
        color: #1a1a1a;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .chat-container {
        max-width: 800px;
        margin: 0 auto;
        padding: 0 1rem;
        background: #ffffff;
    }
    
    .message {
        margin-bottom: 1.5rem;
        padding: 1rem;
        border-radius: 12px;
        line-height: 1.6;
    }
    
    .user-message {
        background-color: #e3f2fd;
        margin-left: 2rem;
        border: 1px solid #2196f3;
        color: #0d47a1;
    }
    
    .bot-message {
        background-color: #f5f5f5;
        margin-right: 2rem;
        border: 1px solid #9e9e9e;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        color: #212121;
    }
    
    .sources {
        font-size: 0.85rem;
        color: #424242;
        margin-top: 0.5rem;
        padding-top: 0.5rem;
        border-top: 1px solid #bdbdbd;
        font-weight: 500;
    }
    
    /* Asegurar fondo blanco */
    .stApp {
        background-color: #ffffff !important;
    }
    
    .main .block-container {
        background-color: #ffffff;
    }
    
    /* Círculo de carga personalizado */
    .loading-spinner {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid #f3f3f3;
        border-top: 3px solid #2196f3;
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin-right: 10px;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Mejorar contraste de texto */
    .message strong {
        color: #1976d2;
        font-weight: 600;
    }
    
    .bot-message strong {
        color: #424242;
    }
    
    .input-container {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: white;
        padding: 1rem;
        border-top: 1px solid #e5e5e5;
        z-index: 1000;
    }
    
    .sidebar-content {
        padding: 1rem;
    }
    
    .status-indicator {
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        margin-right: 0.5rem;
    }
    
    .status-online {
        background-color: #10b981;
    }
    
    .status-offline {
        background-color: #ef4444;
    }
    
    .login-form {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        border: 1px solid #e5e5e5;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    .stTextInput > div > div > input {
        border-radius: 8px;
        border: 1px solid #d1d5db;
        padding: 0.75rem;
    }
    
    .stButton > button {
        background-color: #1a1a1a;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
        width: 100%;
    }
    
    .stButton > button:hover {
        background-color: #374151;
    }
    
    .stSelectbox > div > div > select {
        border-radius: 8px;
        border: 1px solid #d1d5db;
    }
    
    .processing {
        color: #666;
        font-style: italic;
    }
    
    .error-message {
        color: #ef4444;
        background-color: #fef2f2;
        padding: 0.75rem;
        border-radius: 8px;
        border: 1px solid #fecaca;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Funciones de utilidad
def get_api_status():
    """Obtiene el estado de la API."""
    try:
        response = requests.get(HEALTH_ENDPOINT, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return {"status": "error", "message": "API no disponible"}

def send_question_to_api(question: str, token: str = None):
    """Envía una pregunta a la API y devuelve la respuesta."""
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    payload = {"question": question}
    try:
        start_time = time.time()
        response = requests.post(ASK_ENDPOINT, headers=headers, json=payload, timeout=120)
        response.raise_for_status()
        end_time = time.time()
        data = response.json()
        data["processing_time"] = end_time - start_time
        return data
    except requests.exceptions.RequestException as e:
        return {"error": f"Error al comunicarse con la API: {e}"}

def login_user(user_id: str, role: str):
    """Intenta iniciar sesión y obtener un token."""
    try:
        headers = {"Content-Type": "application/json"}
        payload = {"user_id": user_id, "role": role}
        response = requests.post(LOGIN_ENDPOINT, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Error al iniciar sesión: {e}"}

def get_user_info(token: str):
    """Obtiene información del usuario actual."""
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(ME_ENDPOINT, headers=headers, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return None

# Inicialización del estado de sesión
if "history" not in st.session_state:
    st.session_state.history = []
if "auth_token" not in st.session_state:
    st.session_state.auth_token = None
if "user_info" not in st.session_state:
    st.session_state.user_info = None
if "api_status" not in st.session_state:
    st.session_state.api_status = get_api_status()

# Sidebar para autenticación
with st.sidebar:
    st.markdown("## Sistema de Acceso")
    
    # Estado de la API
    api_status = st.session_state.api_status
    if api_status.get("status") == "healthy":
        st.success("API Online")
        if api_status.get("model_loaded"):
            st.info("Modelo: Cargado")
        else:
            st.warning("Modelo: No disponible")
        st.text(f"Documentos: {api_status.get('documents_count', 0)}")
    else:
        st.error("API Offline")
    
    st.markdown("---")
    
    # Autenticación
    if st.session_state.auth_token:
        st.success("Sesión Activa")
        st.markdown(f"**Usuario:** {st.session_state.user_info.get('user_id', 'N/A')}")
        st.markdown(f"**Rol:** {st.session_state.user_info.get('role', 'N/A')}")
        if st.button("Cerrar Sesión", key="logout", type="secondary"):
            st.session_state.auth_token = None
            st.session_state.user_info = None
            st.rerun()
    else:
        st.markdown("### Iniciar Sesión")
        st.markdown("Selecciona tu rol y haz clic en 'Iniciar Sesión'")
        
        with st.form("login_form"):
            role = st.selectbox("Rol", ["admin", "facilitador", "user"], index=0)
            user_id = st.text_input("Usuario", value=role)
            submitted = st.form_submit_button("Iniciar Sesión", type="primary")
            
            if submitted:
                with st.spinner("Iniciando sesión..."):
                    login_response = login_user(user_id, role)
                    if login_response and "access_token" in login_response:
                        st.session_state.auth_token = login_response["access_token"]
                        st.session_state.user_info = get_user_info(st.session_state.auth_token)
                        st.success("Sesión iniciada correctamente")
                        st.rerun()
                    else:
                        st.error(login_response.get("error", "Error al iniciar sesión"))
        
        st.markdown("---")
        st.markdown("### Credenciales")
        st.markdown("- **Admin**: `admin` / `admin`")
        st.markdown("- **Facilitador**: `facilitador` / `facilitador`")
        st.markdown("- **Usuario**: `user` / `user`")

# Contenido principal
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">Asistente para Facilitadores Judiciales</div>', unsafe_allow_html=True)

# Mostrar historial de chat
for i, (q, a, sources, time_taken) in enumerate(st.session_state.history):
    # Mensaje del usuario
    st.markdown(f'<div class="message user-message"><strong>Usted:</strong><br>{q}</div>', unsafe_allow_html=True)
    
    # Respuesta del bot
    st.markdown(f'<div class="message bot-message"><strong>Asistente:</strong><br>{a}</div>', unsafe_allow_html=True)
    
    # Fuentes y tiempo
    if sources:
        # Extraer nombres de archivos de las fuentes (pueden ser strings o dicts)
        source_names = []
        for source in sources:
            if isinstance(source, dict):
                source_names.append(source.get('filename', source.get('source', 'Desconocido')))
            else:
                source_names.append(str(source))
        sources_text = ", ".join(source_names)
        st.markdown(f'<div class="sources">Fuentes: {sources_text}</div>', unsafe_allow_html=True)
    
    if time_taken:
        st.markdown(f'<div class="sources">Tiempo: {time_taken:.2f}s</div>', unsafe_allow_html=True)
    
    st.markdown("---")

# Input de usuario
st.markdown('<div class="input-container">', unsafe_allow_html=True)

if not st.session_state.auth_token:
    st.info("Por favor, inicia sesión en el panel lateral para hacer preguntas.")
else:
    question = st.text_input(
        "Escribe aquí...",
        key="user_input",
        placeholder="Escribe aquí...",
        label_visibility="collapsed"
    )
    
    if question:
        if st.button("Enviar", key="send_button"):
            # Mostrar indicador de procesamiento con círculo de carga
            with st.spinner("Procesando..."):
                response_data = send_question_to_api(question, st.session_state.auth_token)
            
            if "error" in response_data:
                st.error(response_data["error"])
            else:
                answer = response_data.get("answer", "No se pudo obtener una respuesta.")
                sources = response_data.get("sources", [])
                processing_time = response_data.get("processing_time")
                
                # Agregar al historial
                st.session_state.history.append((question, answer, sources, processing_time))
                st.rerun()

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(
    '<div style="text-align: center; color: #666; font-size: 0.85rem; padding: 1rem;">Sistema de Asistencia para Facilitadores Judiciales</div>',
    unsafe_allow_html=True
)
