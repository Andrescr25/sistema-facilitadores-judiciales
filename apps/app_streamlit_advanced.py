#!/usr/bin/env python3
"""
Interfaz web avanzada para el bot de Facilitadores Judiciales.
Incluye autenticación, administración de documentos y chat interactivo.
"""

import streamlit as st
import requests
import json
import time
import os
import subprocess
from datetime import datetime
from typing import List, Dict, Any
import tempfile
import shutil

# Configuración de la página
st.set_page_config(
    page_title="Bot de Facilitadores Judiciales",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configuración
API_URL = os.getenv("API_URL", "http://localhost:8000")
HEALTH_ENDPOINT = f"{API_URL}/health"
ASK_ENDPOINT = f"{API_URL}/ask"
LOGIN_ENDPOINT = f"{API_URL}/auth/login"
ME_ENDPOINT = f"{API_URL}/auth/me"
DEV_TOKENS_ENDPOINT = f"{API_URL}/auth/dev-tokens"

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f4e79;
        text-align: center;
        margin-bottom: 2rem;
        padding: 1rem;
        background: linear-gradient(90deg, #1f4e79, #2e5a8a);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
        margin-left: 20%;
    }
    
    .bot-message {
        background-color: #f3e5f5;
        border-left: 4px solid #9c27b0;
        margin-right: 20%;
    }
    
    .source-item {
        background-color: #f8f9fa;
        padding: 0.5rem;
        border-radius: 5px;
        margin: 0.25rem 0;
        border-left: 3px solid #28a745;
        font-size: 0.9rem;
    }
    
    .status-indicator {
        display: inline-block;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        margin-right: 8px;
    }
    
    .status-online {
        background-color: #28a745;
    }
    
    .status-offline {
        background-color: #dc3545;
    }
    
    .admin-panel {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #dee2e6;
        text-align: center;
    }
    
    .sidebar-content {
        padding: 1rem;
    }
    
    .footer {
        text-align: center;
        color: #6c757d;
        font-size: 0.8rem;
        margin-top: 2rem;
        padding: 1rem;
        border-top: 1px solid #dee2e6;
    }
    
    .upload-section {
        border: 2px dashed #dee2e6;
        border-radius: 8px;
        padding: 2rem;
        text-align: center;
        margin: 1rem 0;
    }
    
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 0.75rem;
        border-radius: 4px;
        border: 1px solid #c3e6cb;
        margin: 1rem 0;
    }
    
    .error-message {
        background-color: #f8d7da;
        color: #721c24;
        padding: 0.75rem;
        border-radius: 4px;
        border: 1px solid #f5c6cb;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def check_api_health() -> Dict[str, Any]:
    """Verifica el estado de la API."""
    try:
        response = requests.get(HEALTH_ENDPOINT, timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            return {"status": "error", "message": f"API error: {response.status_code}"}
    except Exception as e:
        return {"status": "error", "message": f"Connection error: {str(e)}"}

def login_user(user_id: str, role: str) -> Dict[str, Any]:
    """Inicia sesión y obtiene un token."""
    try:
        response = requests.post(
            LOGIN_ENDPOINT,
            json={"user_id": user_id, "role": role},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Login failed: {response.status_code}"}
    except Exception as e:
        return {"error": f"Connection error: {str(e)}"}

def get_user_info(token: str) -> Dict[str, Any]:
    """Obtiene información del usuario actual."""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(ME_ENDPOINT, headers=headers, timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Failed to get user info: {response.status_code}"}
    except Exception as e:
        return {"error": f"Connection error: {str(e)}"}

def ask_question(question: str, token: str = None) -> Dict[str, Any]:
    """Envía una pregunta a la API y devuelve la respuesta."""
    try:
        headers = {"Content-Type": "application/json"}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        
        payload = {"question": question}
        response = requests.post(
            ASK_ENDPOINT,
            json=payload,
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            return {
                "answer": f"Error: {response.status_code} - {response.text}",
                "sources": [],
                "processing_time": 0.0
            }
    except Exception as e:
        return {
            "answer": f"Error de conexión: {str(e)}",
            "sources": [],
            "processing_time": 0.0
        }

def run_ingestion() -> Dict[str, Any]:
    """Ejecuta el script de ingesta de documentos."""
    try:
        result = subprocess.run(
            ["python", "ingest.py"],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            return {"success": True, "message": "Ingesta completada exitosamente", "output": result.stdout}
        else:
            return {"success": False, "message": "Error en la ingesta", "error": result.stderr}
    except subprocess.TimeoutExpired:
        return {"success": False, "message": "La ingesta tardó demasiado tiempo"}
    except Exception as e:
        return {"success": False, "message": f"Error ejecutando ingesta: {str(e)}"}

def initialize_session_state():
    """Inicializa el estado de la sesión."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "api_status" not in st.session_state:
        st.session_state.api_status = check_api_health()
    
    if "auth_token" not in st.session_state:
        st.session_state.auth_token = None
    
    if "user_info" not in st.session_state:
        st.session_state.user_info = None
    
    if "show_login" not in st.session_state:
        st.session_state.show_login = True

def display_login_form():
    """Muestra el formulario de login."""
    st.markdown("## 🔐 Iniciar Sesión")
    
    with st.form("login_form"):
        user_id = st.text_input("Usuario", value="admin")
        role = st.selectbox("Rol", ["admin", "facilitador", "user"], index=0)
        submitted = st.form_submit_button("Iniciar Sesión", use_container_width=True)
        
        if submitted:
            with st.spinner("Iniciando sesión..."):
                login_response = login_user(user_id, role)
                
                if "error" in login_response:
                    st.error(f"Error al iniciar sesión: {login_response['error']}")
                else:
                    st.session_state.auth_token = login_response["access_token"]
                    st.session_state.user_info = get_user_info(st.session_state.auth_token)
                    st.session_state.show_login = False
                    st.success("¡Sesión iniciada exitosamente!")
                    st.rerun()

def display_sidebar():
    """Muestra la barra lateral con información del sistema."""
    with st.sidebar:
        # Estado de la API
        st.markdown("## 📊 Estado del Sistema")
        status = st.session_state.api_status
        
        if status["status"] == "healthy":
            st.markdown("""
            <div class="status-indicator status-online"></div>
            <strong>API Online</strong>
            """, unsafe_allow_html=True)
            
            # Mostrar métricas
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Documentos", status.get("documents_count", 0))
            with col2:
                st.metric("DB Vectorial", "✅" if status.get("vector_db_loaded") else "❌")
        else:
            st.markdown("""
            <div class="status-indicator status-offline"></div>
            <strong>API Offline</strong>
            """, unsafe_allow_html=True)
            st.error(f"Error: {status.get('message', 'Unknown error')}")
        
        st.markdown("---")
        
        # Información del usuario
        if st.session_state.user_info:
            st.markdown("## 👤 Usuario Actual")
            user_info = st.session_state.user_info
            st.success(f"**{user_info.get('user_id', 'N/A')}** ({user_info.get('role', 'N/A')})")
            
            # Mostrar permisos
            permissions = user_info.get('permissions', {})
            st.markdown("**Permisos:**")
            for perm, has_perm in permissions.items():
                if has_perm:
                    st.markdown(f"✅ {perm}")
            
            if st.button("🚪 Cerrar Sesión", use_container_width=True):
                st.session_state.auth_token = None
                st.session_state.user_info = None
                st.session_state.show_login = True
                st.rerun()
        else:
            st.markdown("## 👤 No autenticado")
            if st.button("🔐 Iniciar Sesión", use_container_width=True):
                st.session_state.show_login = True
                st.rerun()
        
        st.markdown("---")
        
        # Botones de control
        st.markdown("## 🛠️ Controles")
        
        if st.button("🔄 Actualizar estado", use_container_width=True):
            st.session_state.api_status = check_api_health()
            st.rerun()
        
        if st.button("🗑️ Limpiar chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

def display_admin_panel():
    """Muestra el panel de administración."""
    if not st.session_state.user_info or st.session_state.user_info.get('role') != 'admin':
        return
    
    st.markdown("## 🔧 Panel de Administración")
    
    # Pestañas para diferentes funciones de admin
    tab1, tab2, tab3 = st.tabs(["📁 Gestión de Documentos", "📊 Estadísticas", "⚙️ Configuración"])
    
    with tab1:
        st.markdown("### Cargar Nuevos Documentos")
        
        # Upload de archivos
        uploaded_files = st.file_uploader(
            "Selecciona archivos para cargar",
            type=['txt', 'pdf', 'docx'],
            accept_multiple_files=True,
            help="Formatos soportados: TXT, PDF, DOCX"
        )
        
        if uploaded_files:
            st.markdown(f"**{len(uploaded_files)} archivo(s) seleccionado(s):**")
            for file in uploaded_files:
                st.markdown(f"- {file.name} ({file.size} bytes)")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("💾 Guardar Archivos", use_container_width=True):
                if uploaded_files:
                    # Crear directorio de datos si no existe
                    data_dir = "data/docs"
                    os.makedirs(data_dir, exist_ok=True)
                    
                    saved_files = []
                    for file in uploaded_files:
                        file_path = os.path.join(data_dir, file.name)
                        with open(file_path, "wb") as f:
                            f.write(file.getbuffer())
                        saved_files.append(file.name)
                    
                    st.success(f"✅ {len(saved_files)} archivo(s) guardado(s) exitosamente")
                    st.session_state.saved_files = saved_files
                else:
                    st.warning("No hay archivos seleccionados")
        
        with col2:
            if st.button("🔄 Procesar Documentos", use_container_width=True):
                with st.spinner("Procesando documentos..."):
                    result = run_ingestion()
                
                if result["success"]:
                    st.success(result["message"])
                    st.session_state.api_status = check_api_health()  # Actualizar estado
                else:
                    st.error(f"Error: {result['message']}")
                    if "error" in result:
                        st.code(result["error"])
        
        # Mostrar archivos existentes
        st.markdown("### Archivos Existentes")
        data_dir = "data/docs"
        if os.path.exists(data_dir):
            files = [f for f in os.listdir(data_dir) if f.endswith(('.txt', '.pdf', '.docx'))]
            if files:
                for file in files:
                    file_path = os.path.join(data_dir, file)
                    file_size = os.path.getsize(file_path)
                    col1, col2, col3 = st.columns([3, 1, 1])
                    with col1:
                        st.markdown(f"📄 {file}")
                    with col2:
                        st.markdown(f"{file_size:,} bytes")
                    with col3:
                        if st.button("🗑️", key=f"delete_{file}", help="Eliminar archivo"):
                            try:
                                os.remove(file_path)
                                st.success(f"Archivo {file} eliminado")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error eliminando archivo: {e}")
            else:
                st.info("No hay archivos en el directorio de datos")
        else:
            st.info("El directorio de datos no existe")
    
    with tab2:
        st.markdown("### Estadísticas del Sistema")
        
        # Métricas básicas
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Documentos Indexados", st.session_state.api_status.get("documents_count", 0))
        
        with col2:
            st.metric("Mensajes en Chat", len(st.session_state.messages))
        
        with col3:
            st.metric("Estado API", "✅ Online" if st.session_state.api_status.get("status") == "healthy" else "❌ Offline")
        
        # Información adicional
        st.markdown("### Información Técnica")
        st.json(st.session_state.api_status)
    
    with tab3:
        st.markdown("### Configuración del Sistema")
        
        st.markdown("**Variables de Entorno:**")
        env_vars = {
            "API_URL": API_URL,
            "MODEL_PATH": os.getenv("MODEL_PATH", "No configurado"),
            "VECTOR_DB_DIR": os.getenv("VECTOR_DB_DIR", "./data/chroma"),
            "DATA_DIR": os.getenv("DATA_DIR", "./data/docs")
        }
        
        for key, value in env_vars.items():
            st.markdown(f"- **{key}**: `{value}`")
        
        st.markdown("**Acciones del Sistema:**")
        
        if st.button("🔄 Reiniciar API", use_container_width=True):
            st.info("Para reiniciar la API, detén y vuelve a ejecutar el servidor")
        
        if st.button("🧹 Limpiar Base de Datos", use_container_width=True):
            st.warning("Esta acción eliminará todos los documentos indexados. ¿Estás seguro?")
            if st.button("✅ Confirmar Limpieza", type="primary"):
                try:
                    import shutil
                    shutil.rmtree("data/chroma", ignore_errors=True)
                    st.success("Base de datos limpiada")
                    st.session_state.api_status = check_api_health()
                except Exception as e:
                    st.error(f"Error limpiando base de datos: {e}")

def display_chat_interface():
    """Muestra la interfaz principal de chat."""
    # Header principal
    st.markdown('<h1 class="main-header">⚖️ Bot de Facilitadores Judiciales</h1>', unsafe_allow_html=True)
    
    # Mostrar mensajes del chat
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            # Mostrar fuentes si es un mensaje del bot
            if message["role"] == "assistant" and "sources" in message:
                with st.expander("📚 Fuentes consultadas"):
                    for i, source in enumerate(message["sources"], 1):
                        st.markdown(f"""
                        <div class="source-item">
                            <strong>{i}. {source.get('filename', 'Desconocido')}</strong><br>
                            <small>{source.get('content', '')}</small>
                        </div>
                        """, unsafe_allow_html=True)
    
    # Input de chat
    if prompt := st.chat_input("Escribe tu pregunta sobre facilitación judicial..."):
        # Verificar autenticación
        if not st.session_state.auth_token:
            st.warning("Por favor, inicia sesión para hacer preguntas.")
            return
        
        # Agregar mensaje del usuario
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Mostrar mensaje del usuario
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generar respuesta del bot
        with st.chat_message("assistant"):
            with st.spinner("🤔 Procesando tu pregunta..."):
                response = ask_question(prompt, st.session_state.auth_token)
            
            # Mostrar respuesta
            st.markdown(response["answer"])
            
            # Mostrar fuentes
            if response["sources"]:
                with st.expander("📚 Fuentes consultadas"):
                    for i, source in enumerate(response["sources"], 1):
                        st.markdown(f"""
                        <div class="source-item">
                            <strong>{i}. {source.get('filename', 'Desconocido')}</strong><br>
                            <small>{source.get('content', '')}</small>
                        </div>
                        """, unsafe_allow_html=True)
            
            # Mostrar tiempo de procesamiento
            st.caption(f"⏱️ Tiempo de procesamiento: {response['processing_time']:.2f}s")
        
        # Guardar mensaje del bot
        st.session_state.messages.append({
            "role": "assistant", 
            "content": response["answer"],
            "sources": response["sources"],
            "processing_time": response["processing_time"]
        })

def display_example_questions():
    """Muestra preguntas de ejemplo."""
    st.markdown("### 💡 Preguntas de ejemplo")
    
    example_questions = [
        "¿Cuáles son los requisitos para ser facilitador judicial?",
        "¿Cuánto dura el procedimiento de conciliación?",
        "¿Qué técnicas de facilitación se recomiendan?",
        "¿Cuáles son los costos del procedimiento?",
        "¿Cuáles son las fases del procedimiento de conciliación?",
        "¿Qué es la conciliación judicial?",
        "¿Cuáles son las obligaciones del facilitador?",
        "¿Qué sanciones puede recibir un facilitador?"
    ]
    
    cols = st.columns(2)
    for i, question in enumerate(example_questions):
        with cols[i % 2]:
            if st.button(question, key=f"example_{i}", use_container_width=True):
                if not st.session_state.auth_token:
                    st.warning("Por favor, inicia sesión para hacer preguntas.")
                else:
                    # Simular pregunta
                    st.session_state.messages.append({"role": "user", "content": question})
                    st.rerun()

def main():
    """Función principal de la aplicación."""
    # Inicializar estado
    initialize_session_state()
    
    # Mostrar login si es necesario
    if st.session_state.show_login:
        display_login_form()
        return
    
    # Mostrar sidebar
    display_sidebar()
    
    # Mostrar panel de admin si es admin
    if st.session_state.user_info and st.session_state.user_info.get('role') == 'admin':
        display_admin_panel()
        st.markdown("---")
    
    # Mostrar interfaz principal
    display_chat_interface()
    
    # Mostrar preguntas de ejemplo si no hay mensajes
    if not st.session_state.messages:
        st.markdown("---")
        display_example_questions()
    
    # Footer
    st.markdown("""
    <div class="footer">
        <p>Bot de Facilitadores Judiciales v1.0.0 | Desarrollado con Streamlit y FastAPI</p>
        <p>Para soporte técnico, contacta al administrador del sistema</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
