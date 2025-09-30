#!/usr/bin/env python3
"""
Chat FJ - Servicio Nacional de Facilitadoras y Facilitadores Judiciales
Interfaz web estilo ChatGPT con historial de conversaciones
"""

import streamlit as st
import requests
import time
import uuid
from datetime import datetime
from typing import List, Dict, Optional

# Configuración de la página
st.set_page_config(
    page_title="Chat FJ | Poder Judicial Costa Rica",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS Moderno estilo ChatGPT
st.markdown("""
<style>
    /* Importar fuente profesional */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Variables de color */
    :root {
        --primary: #1e40af;
        --primary-light: #3b82f6;
        --border: #e5e7eb;
        --text-dark: #1f2937;
        --text-light: #6b7280;
        --bg-user: #2563eb;
        --bg-assistant: #f3f4f6;
        --shadow: rgba(0, 0, 0, 0.1);
        --sidebar-bg: #f9fafb;
        --hover-bg: #f3f4f6;
    }
    
    /* Reset */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    /* Ocultar elementos de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Sidebar personalizado estilo ChatGPT */
    [data-testid="stSidebar"] {
        background: var(--sidebar-bg);
        border-right: 1px solid var(--border);
        padding: 0;
    }
    
    [data-testid="stSidebar"] > div:first-child {
        padding: 1rem 0.75rem;
    }
    
    /* Botón nueva conversación en sidebar */
    .new-chat-btn {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.75rem 1rem;
        margin: 0.5rem 0 1rem 0;
        background: white;
        border: 1px solid var(--border);
        border-radius: 0.5rem;
        cursor: pointer;
        font-weight: 500;
        font-size: 0.875rem;
        transition: all 0.2s;
        width: 100%;
        text-align: left;
    }
    
    .new-chat-btn:hover {
        background: #f9fafb;
        border-color: var(--primary-light);
    }
    
    /* Items de conversación */
    .conversation-item {
        padding: 0.75rem;
        margin: 0.25rem 0;
        border-radius: 0.5rem;
        cursor: pointer;
        transition: all 0.2s;
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 0.875rem;
        color: var(--text-dark);
        background: transparent;
    }
    
    .conversation-item:hover {
        background: var(--hover-bg);
    }
    
    .conversation-item.active {
        background: white;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    
    .conversation-title {
        flex: 1;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        font-weight: 500;
    }
    
    .conversation-date {
        font-size: 0.75rem;
        color: var(--text-light);
        margin-top: 0.25rem;
    }
    
    /* Header minimalista */
    .main-header {
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
        padding: 1.25rem 2rem;
        margin: -6rem -4rem 0 -4rem;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        position: sticky;
        top: 0;
        z-index: 100;
    }
    
    .main-header h1 {
        color: white;
        font-size: 1.5rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.02em;
    }
    
    .main-header p {
        color: rgba(255, 255, 255, 0.9);
        font-size: 0.85rem;
        margin: 0.25rem 0 0 0;
        font-weight: 400;
    }
    
    /* Contenedor principal */
    .main .block-container {
        max-width: 900px;
        padding: 0 2rem 1rem 2rem;
        background: white;
    }
    
    /* Chat container */
    .chat-container {
        padding: 1.5rem 0 2rem 0;
        margin: 0;
        min-height: calc(100vh - 300px);
        max-height: calc(100vh - 300px);
        overflow-y: auto;
        border: none;
        background: transparent;
    }
    
    /* Mensajes mejorados estilo ChatGPT */
    .message {
        margin: 1rem 0;
        padding: 1rem 1.25rem;
        border-radius: 1.125rem;
        max-width: 75%;
        line-height: 1.6;
        font-size: 0.95rem;
        animation: fadeInUp 0.3s ease-out;
        box-shadow: 0 1px 3px var(--shadow);
        position: relative;
    }
    
    @keyframes fadeInUp {
        from { 
            opacity: 0; 
            transform: translateY(10px);
        }
        to { 
            opacity: 1; 
            transform: translateY(0);
        }
    }
    
    .user-message {
        background: var(--bg-user);
        color: white;
        margin-left: auto;
        border-bottom-right-radius: 0.375rem;
        box-shadow: 0 2px 6px rgba(37, 99, 235, 0.3);
    }
    
    .assistant-message {
        background: white;
        color: var(--text-dark);
        margin-right: auto;
        border-bottom-left-radius: 0.375rem;
        border: 1px solid #e5e7eb;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
    }
    
    /* Input section fijo al fondo */
    .input-section {
        position: sticky;
        bottom: 0;
        background: white;
        padding: 1.5rem 0 1rem 0;
        margin: 0 -2rem;
        padding-left: 2rem;
        padding-right: 2rem;
        border-top: 1px solid var(--border);
        z-index: 50;
    }
    
    .stTextInput input {
        border: 2px solid var(--border);
        border-radius: 1.5rem;
        padding: 0.875rem 1.125rem;
        font-size: 0.95rem;
        transition: all 0.2s;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }
    
    .stTextInput input:focus {
        border-color: var(--primary-light);
        box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1);
        outline: none;
    }
    
    /* Botones del sidebar */
    .sidebar .stButton button {
        background: white;
        color: var(--text-dark);
        border: 1px solid var(--border);
        padding: 0.625rem 1rem;
        border-radius: 0.5rem;
        font-weight: 500;
        font-size: 0.875rem;
        transition: all 0.2s;
        width: 100%;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    }
    
    .sidebar .stButton button:hover {
        background: #f9fafb;
        border-color: var(--primary-light);
    }
    
    /* Footer estilo ChatGPT */
    .footer-disclaimer {
        background: transparent;
        padding: 0.75rem 0;
        text-align: center;
        font-size: 0.75rem;
        color: #9ca3af;
        margin-top: 1rem;
    }
    
    /* Loading */
    .stSpinner > div {
        border-top-color: var(--primary) !important;
    }
    
    /* Scroll suave */
    .chat-container {
        scroll-behavior: smooth;
    }
    
    .chat-container::-webkit-scrollbar {
        width: 6px;
    }
    
    .chat-container::-webkit-scrollbar-track {
        background: transparent;
    }
    
    .chat-container::-webkit-scrollbar-thumb {
        background: #d1d5db;
        border-radius: 3px;
    }
    
    .chat-container::-webkit-scrollbar-thumb:hover {
        background: #9ca3af;
    }
    
    /* Welcome screen */
    .welcome-screen {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 50vh;
        text-align: center;
        padding: 2rem;
    }
    
    .welcome-screen h2 {
        color: var(--text-dark);
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .welcome-screen p {
        color: var(--text-light);
        font-size: 1rem;
        margin-bottom: 2rem;
    }
    
    .welcome-examples {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin-top: 2rem;
        width: 100%;
        max-width: 600px;
    }
    
    .example-card {
        background: white;
        border: 1px solid var(--border);
        border-radius: 0.75rem;
        padding: 1rem;
        cursor: pointer;
        transition: all 0.2s;
        text-align: left;
    }
    
    .example-card:hover {
        border-color: var(--primary-light);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        transform: translateY(-2px);
    }
    
    .example-card h4 {
        color: var(--text-dark);
        font-size: 0.875rem;
        font-weight: 600;
        margin: 0 0 0.5rem 0;
    }
    
    .example-card p {
        color: var(--text-light);
        font-size: 0.8rem;
        margin: 0;
        line-height: 1.4;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .main-header {
            padding: 1rem;
            margin: -4rem -1rem 0 -1rem;
        }
        
        .main-header h1 {
            font-size: 1.25rem;
        }
        
        .message {
            max-width: 85%;
        }
        
        .main .block-container {
            padding: 0 1rem 1rem 1rem;
        }
        
        .input-section {
            margin: 0 -1rem;
            padding-left: 1rem;
            padding-right: 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Configuración API
API_URL = "http://localhost:8000"

def ask_question(question: str, history: List[Dict]) -> Dict:
    """Enviar pregunta a la API."""
    try:
        response = requests.post(
            f"{API_URL}/ask",
            json={"question": question, "history": history},
            timeout=30
        )
        if response.status_code == 200:
            return response.json()
        return {"answer": f"Error: {response.status_code}", "sources": []}
    except Exception as e:
        return {"answer": f"Error de conexión: {str(e)}", "sources": []}

def create_new_conversation() -> Dict:
    """Crear una nueva conversación."""
    return {
        "id": str(uuid.uuid4()),
        "title": "Nueva conversación",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "messages": []
    }

def update_conversation_title(conversation: Dict):
    """Actualizar el título de la conversación basado en el primer mensaje del usuario."""
    user_messages = [m for m in conversation["messages"] if m["role"] == "user"]
    if user_messages:
        first_msg = user_messages[0]["content"]
        # Tomar primeras 30 caracteres
        conversation["title"] = first_msg[:30] + ("..." if len(first_msg) > 30 else "")

def format_timestamp(timestamp_str: str) -> str:
    """Formatear timestamp de forma amigable."""
    try:
        dt = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
        now = datetime.now()
        diff = now - dt
        
        if diff.days == 0:
            return "Hoy"
        elif diff.days == 1:
            return "Ayer"
        elif diff.days < 7:
            return f"Hace {diff.days} días"
        else:
            return dt.strftime("%d/%m/%Y")
    except:
        return timestamp_str

def main():
    """Aplicación principal."""
    
    # Inicializar estado de sesión
    if "conversations" not in st.session_state:
        st.session_state.conversations = [create_new_conversation()]
    
    if "current_conversation_id" not in st.session_state:
        st.session_state.current_conversation_id = st.session_state.conversations[0]["id"]
    
    if "last_input" not in st.session_state:
        st.session_state.last_input = ""
    
    # Sidebar con historial de conversaciones
    with st.sidebar:
        st.markdown("### 💬 Conversaciones")
        
        # Botón para nueva conversación
        if st.button("➕ Nueva conversación", key="new_chat_btn", use_container_width=True):
            new_conv = create_new_conversation()
            st.session_state.conversations.insert(0, new_conv)
            st.session_state.current_conversation_id = new_conv["id"]
            st.session_state.last_input = ""
            st.rerun()
        
        st.markdown("---")
        
        # Mostrar lista de conversaciones
        for idx, conv in enumerate(st.session_state.conversations):
            is_active = conv["id"] == st.session_state.current_conversation_id
            
            col1, col2 = st.columns([5, 1])
            
            with col1:
                if st.button(
                    f"💬 {conv['title'][:25]}{'...' if len(conv['title']) > 25 else ''}",
                    key=f"conv_{conv['id']}",
                    use_container_width=True,
                    type="primary" if is_active else "secondary"
                ):
                    st.session_state.current_conversation_id = conv["id"]
                    st.session_state.last_input = ""
                    st.rerun()
            
            with col2:
                if st.button("🗑️", key=f"delete_{conv['id']}", use_container_width=True):
                    if len(st.session_state.conversations) > 1:
                        st.session_state.conversations.pop(idx)
                        if conv["id"] == st.session_state.current_conversation_id:
                            st.session_state.current_conversation_id = st.session_state.conversations[0]["id"]
                        st.rerun()
            
            # Mostrar timestamp
            if conv["timestamp"]:
                st.caption(f"📅 {format_timestamp(conv['timestamp'])}")
        
        st.markdown("---")
        st.markdown("""
        <div style="font-size: 0.75rem; color: #9ca3af; text-align: center;">
            <p>Chat FJ v2.0</p>
            <p>Poder Judicial CR 🇨🇷</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>⚖️ Chat FJ</h1>
        <p>Servicio Nacional de Facilitadoras y Facilitadores Judiciales</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Obtener conversación actual
    current_conv = next((c for c in st.session_state.conversations if c["id"] == st.session_state.current_conversation_id), None)
    
    if not current_conv:
        st.error("No se encontró la conversación")
        return
    
    # Si no hay mensajes, mostrar welcome screen
    if len(current_conv["messages"]) == 0:
        st.markdown("""
        <div class="welcome-screen">
            <h2>👋 ¡Hola! Soy Chat FJ</h2>
            <p>¿En qué puedo ayudarte hoy?</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Ejemplos de preguntas
        st.markdown("### 💡 Ejemplos de consultas:")
        col1, col2, col3 = st.columns(3)
        
        examples = [
            ("💰 Pensión alimentaria", "Mi ex no paga pensión, ¿qué hago?"),
            ("⚖️ Conciliación", "¿Cuánto dura una conciliación?"),
            ("👔 Problemas laborales", "Mi jefe no me paga horas extra")
        ]
        
        for col, (title, example) in zip([col1, col2, col3], examples):
            with col:
                if st.button(title, key=f"example_{title}", use_container_width=True):
                    # Simular que el usuario escribió este ejemplo
                    st.session_state.last_input = example
                    st.rerun()
    
    # Contenedor de chat
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Mostrar mensajes
    for message in current_conv["messages"]:
        if message["role"] == "user":
            st.markdown(
                f'<div class="message user-message">{message["content"]}</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f'<div class="message assistant-message">{message["content"]}</div>',
                unsafe_allow_html=True
            )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Input section fija al fondo
    st.markdown('<div class="input-section"></div>', unsafe_allow_html=True)
    
    # Input de texto
    input_key = f"user_input_{current_conv['id']}_{len(current_conv['messages'])}"
    user_input = st.text_input(
        "Escribe tu pregunta...",
        key=input_key,
        label_visibility="collapsed",
        placeholder="Envía un mensaje a Chat FJ... (Presiona Enter para enviar)"
    )
    
    # Procesar pregunta SOLO si es diferente al último input procesado
    if user_input and user_input.strip() and user_input != st.session_state.last_input:
        # Guardar este input como procesado
        st.session_state.last_input = user_input
        
        # Agregar mensaje del usuario
        current_conv["messages"].append({"role": "user", "content": user_input})
        
        # Actualizar timestamp de la conversación
        current_conv["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Actualizar título si es el primer mensaje
        if len(current_conv["messages"]) == 1:
            update_conversation_title(current_conv)
        
        # Mostrar mensaje del usuario inmediatamente
        st.markdown(
            f'<div class="message user-message">{user_input}</div>',
            unsafe_allow_html=True
        )
        
        # Preparar historial para la API
        history = [
            {"role": msg["role"], "content": msg["content"]}
            for msg in current_conv["messages"][:-1]  # Excluir última pregunta
        ]
        
        # Obtener respuesta del API
        with st.spinner("⚖️ Pensando..."):
            response = ask_question(user_input, history)
            answer = response.get("answer", "No se obtuvo respuesta")
        
        # Crear placeholder para la animación de escritura
        message_placeholder = st.empty()
        full_response = ""
        
        # Simular escritura palabra por palabra (estilo ChatGPT)
        words = answer.split()
        for i, word in enumerate(words):
            full_response += word + " "
            # Mostrar el texto con cursor parpadeante
            message_placeholder.markdown(
                f'<div class="message assistant-message">{full_response}▌</div>',
                unsafe_allow_html=True
            )
            time.sleep(0.03)  # Delay entre palabras (30ms)
        
        # Mostrar respuesta final sin cursor
        message_placeholder.markdown(
            f'<div class="message assistant-message">{answer}</div>',
            unsafe_allow_html=True
        )
        
        # Agregar respuesta al historial
        current_conv["messages"].append({"role": "assistant", "content": answer})
        
        # Pequeña pausa antes de permitir siguiente mensaje
        time.sleep(0.5)
        
        # Resetear el último input para permitir nuevos mensajes
        st.session_state.last_input = ""
        
        # Recargar para actualizar la interfaz
        st.rerun()
    
    # Footer estilo ChatGPT
    st.markdown("""
    <div class="footer-disclaimer">
        Chat FJ puede cometer errores. Verifica la información importante con fuentes oficiales.
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()