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
    
    /* Variables de color estilo Claude */
    :root {
        --primary: #676767;
        --primary-light: #8b8b8b;
        --border: #e0e0e0;
        --text-dark: #2c2c2c;
        --text-light: #666666;
        --bg-user: #f4f4f4;
        --bg-assistant: #ffffff;
        --shadow: rgba(0, 0, 0, 0.04);
        --sidebar-bg: #f7f7f8;
        --hover-bg: #ebebeb;
        --accent: #d97706;
    }
    
    /* Reset */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    /* Ocultar elementos de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Sidebar minimalista estilo Claude */
    [data-testid="stSidebar"] {
        background: #f7f7f8;
        border-right: 1px solid #e0e0e0;
        padding: 0;
    }
    
    [data-testid="stSidebar"] > div:first-child {
        padding: 0.75rem;
    }
    
    /* Título del sidebar */
    .sidebar-title {
        color: #fff;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        padding: 0.5rem 0.75rem;
        margin-bottom: 0.5rem;
        opacity: 0.7;
    }
    
    /* Items de conversación estilo Claude */
    .conversation-item {
        padding: 0.5rem 0.625rem;
        margin: 0.125rem 0;
        border-radius: 0.375rem;
        cursor: pointer;
        transition: all 0.15s ease;
        font-size: 0.8rem;
        color: #2c2c2c;
        background: transparent;
        border: none;
        position: relative;
        overflow: hidden;
    }
    
    .conversation-item:hover {
        background: #ebebeb;
    }
    
    .conversation-item.active {
        background: #e5e5e5;
        color: #2c2c2c;
    }
    
    .conversation-title {
        flex: 1;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        font-weight: 400;
    }
    
    .conversation-date {
        font-size: 0.7rem;
        color: #9ca3af;
        margin-top: 0.125rem;
        opacity: 0.7;
    }
    
    /* Header estilo Claude - minimalista */
    .main-header {
        background: #ffffff;
        padding: 0.875rem 1.5rem;
        margin: -6rem -4rem 0 -4rem;
        text-align: left;
        border-bottom: 1px solid #e0e0e0;
        position: sticky;
        top: 0;
        z-index: 100;
    }
    
    .main-header h1 {
        color: #2c2c2c;
        font-size: 1rem;
        font-weight: 500;
        margin: 0;
        letter-spacing: -0.01em;
    }
    
    .main-header p {
        color: #666666;
        font-size: 0.75rem;
        margin: 0.125rem 0 0 0;
        font-weight: 400;
    }
    
    /* Contenedor principal estilo Claude */
    .main .block-container {
        max-width: 48rem;
        padding: 0 2rem 0.5rem 2rem;
        background: #ffffff;
    }
    
    /* Chat container sin scroll */
    .chat-container {
        padding: 0.25rem 0 0.25rem 0;
        margin: 0;
        min-height: calc(100vh - 180px);
        max-height: calc(100vh - 180px);
        overflow-y: auto;
        border: none;
        background: transparent;
    }
    
    /* Mensajes estilo Claude - ultra minimalista */
    .message {
        margin: 1.5rem 0;
        padding: 0;
        border-radius: 0;
        max-width: 100%;
        line-height: 1.6;
        font-size: 0.9375rem;
        animation: fadeIn 0.3s ease-out;
        box-shadow: none;
        position: relative;
        border-bottom: 1px solid #f0f0f0;
        padding-bottom: 1.5rem;
    }
    
    @keyframes fadeIn {
        from { 
            opacity: 0;
        }
        to { 
            opacity: 1;
        }
    }
    
    .user-message {
        background: transparent;
        color: #2c2c2c;
        margin-left: 0;
        font-weight: 400;
        padding-left: 2.5rem;
        position: relative;
    }
    
    .user-message::before {
        content: "U";
        position: absolute;
        left: 0.5rem;
        top: 0;
        width: 1.5rem;
        height: 1.5rem;
        background: #2c2c2c;
        color: white;
        border-radius: 0.25rem;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.75rem;
        font-weight: 600;
    }
    
    .assistant-message {
        background: transparent;
        color: #2c2c2c;
        margin-right: 0;
        padding-left: 2.5rem;
        position: relative;
    }
    
    .assistant-message::before {
        content: "FJ";
        position: absolute;
        left: 0.5rem;
        top: 0;
        width: 1.5rem;
        height: 1.5rem;
        background: linear-gradient(135deg, #d97706 0%, #f59e0b 100%);
        color: white;
        border-radius: 0.25rem;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.65rem;
        font-weight: 700;
    }
    
    /* Input section pegado */
    .input-section {
        position: sticky;
        bottom: 0;
        background: white;
        padding: 0.375rem 0 0.375rem 0;
        margin: 0 -2rem;
        padding-left: 2rem;
        padding-right: 2rem;
        border-top: 1px solid var(--border);
        z-index: 50;
    }
    
    .stTextInput input {
        border: 1px solid #d0d0d0;
        border-radius: 0.5rem;
        padding: 0.75rem 1rem;
        font-size: 0.9375rem;
        transition: all 0.2s ease;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04);
        background: #ffffff;
    }
    
    .stTextInput input:focus {
        border-color: #a0a0a0;
        box-shadow: 0 0 0 3px rgba(0, 0, 0, 0.05);
        outline: none;
    }
    
    /* Botones del sidebar estilo Claude */
    [data-testid="stSidebar"] .stButton button {
        background: #ffffff;
        color: #2c2c2c;
        border: 1px solid #d0d0d0;
        padding: 0.5rem 0.75rem;
        border-radius: 0.375rem;
        font-weight: 500;
        font-size: 0.8rem;
        transition: all 0.15s ease;
        width: 100%;
    }
    
    [data-testid="stSidebar"] .stButton button:hover {
        background: #f5f5f5;
        border-color: #b0b0b0;
    }
    
    /* Botón nueva conversación destacado */
    [data-testid="stSidebar"] .stButton:first-of-type button {
        background: #2c2c2c;
        border-color: #2c2c2c;
        color: #ffffff;
        font-weight: 600;
    }
    
    [data-testid="stSidebar"] .stButton:first-of-type button:hover {
        background: #1a1a1a;
        border-color: #1a1a1a;
    }
    
    /* Botones de eliminar más discretos */
    [data-testid="stSidebar"] .stButton button[kind="secondary"] {
        padding: 0.375rem 0.5rem;
        font-size: 0.75rem;
        opacity: 0.5;
        border: none;
        background: transparent;
    }
    
    [data-testid="stSidebar"] .stButton button[kind="secondary"]:hover {
        opacity: 1;
        background: #ffebee;
        color: #d32f2f;
    }
    
    /* Footer estilo Claude */
    .footer-disclaimer {
        background: transparent;
        padding: 0.5rem 0;
        text-align: center;
        font-size: 0.75rem;
        color: #999999;
        margin-top: 0.5rem;
        border-top: 1px solid #f0f0f0;
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
    
    /* Welcome screen estilo Claude */
    .welcome-screen {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 30vh;
        text-align: center;
        padding: 2rem 1rem;
    }
    
    .welcome-screen h2 {
        color: #2c2c2c;
        font-size: 1.5rem;
        font-weight: 400;
        margin-bottom: 0.5rem;
        margin-top: 0;
    }
    
    .welcome-screen p {
        color: #666666;
        font-size: 0.9375rem;
        margin-bottom: 2rem;
        margin-top: 0;
    }
    
    .welcome-examples {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        gap: 0.5rem;
        margin-top: 0.5rem;
        width: 100%;
        max-width: 600px;
    }
    
    .example-card {
        background: #ffffff;
        border: 1px solid #d0d0d0;
        border-radius: 0.5rem;
        padding: 0.875rem 1rem;
        cursor: pointer;
        transition: all 0.2s ease;
        text-align: left;
    }
    
    .example-card:hover {
        border-color: #a0a0a0;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.06);
    }
    
    .example-card h4 {
        color: #2c2c2c;
        font-size: 0.8125rem;
        font-weight: 500;
        margin: 0 0 0.375rem 0;
    }
    
    .example-card p {
        color: #666666;
        font-size: 0.8125rem;
        margin: 0;
        line-height: 1.4;
    }
    
    /* Responsive mejorado */
    @media (max-width: 768px) {
        .main-header {
            padding: 0.75rem 1rem;
            margin: -4rem -1rem 0 -1rem;
        }
        
        .main-header h1 {
            font-size: 1.125rem;
        }
        
        .main-header p {
            font-size: 0.7rem;
        }
        
        .message {
            max-width: 85%;
            font-size: 0.8rem;
            padding: 0.5rem 0.75rem;
            margin: 0.375rem 0;
        }
        
        .main .block-container {
            padding: 0 1rem 0.75rem 1rem;
        }
        
        .input-section {
            margin: 0 -1rem;
            padding: 0.5rem 1rem 0.5rem 1rem;
        }
        
        .chat-container {
            min-height: calc(100vh - 160px);
            max-height: calc(100vh - 160px);
            padding: 0.25rem 0;
        }
        
        .stTextInput input {
            font-size: 0.8rem;
            padding: 0.625rem 0.875rem;
        }
        
        .welcome-screen {
            min-height: 20vh;
            padding: 0.5rem 0.25rem;
        }
        
        .welcome-screen h2 {
            font-size: 1.125rem;
        }
        
        .welcome-examples {
            grid-template-columns: 1fr;
            gap: 0.5rem;
        }
        
        [data-testid="stSidebar"] {
            padding: 0;
        }
    }
    
    /* Scroll más delgado en sidebar */
    [data-testid="stSidebar"]::-webkit-scrollbar {
        width: 4px;
    }
    
    [data-testid="stSidebar"]::-webkit-scrollbar-track {
        background: transparent;
    }
    
    [data-testid="stSidebar"]::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.2);
        border-radius: 2px;
    }
    
    [data-testid="stSidebar"]::-webkit-scrollbar-thumb:hover {
        background: rgba(255, 255, 255, 0.3);
    }
    
    /* Captions en sidebar oscuros */
    [data-testid="stSidebar"] .element-container div[data-testid="stCaptionContainer"] {
        color: rgba(255, 255, 255, 0.4) !important;
        font-size: 0.65rem !important;
        margin-top: 0.125rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Eliminar espacios innecesarios en sidebar */
    [data-testid="stSidebar"] .element-container {
        margin-bottom: 0.25rem;
    }
    
    /* Caption específico */
    [data-testid="stSidebar"] p {
        margin-bottom: 0.25rem;
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
        # Verificar si la conversación actual está vacía
        current_conv_temp = next((c for c in st.session_state.conversations if c["id"] == st.session_state.current_conversation_id), None)
        is_current_empty = current_conv_temp and len(current_conv_temp["messages"]) == 0
        
        # Botón para nueva conversación (deshabilitado si actual está vacía)
        if st.button("➕  Nueva conversación", key="new_chat_btn", use_container_width=True, disabled=is_current_empty):
            new_conv = create_new_conversation()
            st.session_state.conversations.insert(0, new_conv)
            st.session_state.current_conversation_id = new_conv["id"]
            st.session_state.last_input = ""
            st.rerun()
        
        # Mostrar mensaje si está deshabilitado
        if is_current_empty:
            st.caption("⚠️ Escribe algo primero")
        
        st.markdown('<div style="height: 1rem;"></div>', unsafe_allow_html=True)
        
        # Mostrar lista de conversaciones
        for idx, conv in enumerate(st.session_state.conversations):
            is_active = conv["id"] == st.session_state.current_conversation_id
            
            col1, col2 = st.columns([5, 1])
            
            with col1:
                # Título más corto y limpio
                title = conv['title'][:30]
                if len(conv['title']) > 30:
                    title += "..."
                
                if st.button(
                    f"💬  {title}",
                    key=f"conv_{conv['id']}",
                    use_container_width=True,
                    type="primary" if is_active else "secondary"
                ):
                    st.session_state.current_conversation_id = conv["id"]
                    st.session_state.last_input = ""
                    st.rerun()
            
            with col2:
                if st.button("🗑️", key=f"delete_{conv['id']}", use_container_width=True, type="secondary"):
                    if len(st.session_state.conversations) > 1:
                        st.session_state.conversations.pop(idx)
                        if conv["id"] == st.session_state.current_conversation_id:
                            st.session_state.current_conversation_id = st.session_state.conversations[0]["id"]
                        st.rerun()
            
            # Timestamp más compacto
            if conv["timestamp"]:
                st.caption(f"🕐 {format_timestamp(conv['timestamp'])}")
        
        # Footer minimalista
        st.markdown('<div style="height: 2rem;"></div>', unsafe_allow_html=True)
        st.markdown("""
        <div style="font-size: 0.65rem; color: rgba(255,255,255,0.4); text-align: center; padding: 0.5rem;">
            <p style="margin: 0; padding: 0;">Chat FJ v2.0</p>
            <p style="margin: 0.25rem 0 0 0; padding: 0;">Poder Judicial CR 🇨🇷</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>Chat FJ</h1>
        <p>Servicio Nacional de Facilitadoras y Facilitadores Judiciales</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Obtener conversación actual
    current_conv = next((c for c in st.session_state.conversations if c["id"] == st.session_state.current_conversation_id), None)
    
    if not current_conv:
        st.error("No se encontró la conversación")
        return
    
    # Si no hay mensajes, mostrar welcome screen compacto
    if len(current_conv["messages"]) == 0:
        st.markdown("""
        <div class="welcome-screen">
            <h2>¿En qué puedo ayudarte hoy?</h2>
            <p>Estoy aquí para orientarte sobre temas legales y judiciales en Costa Rica</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Ejemplos de preguntas estilo Claude
        st.markdown('<p style="text-align: center; font-size: 0.875rem; font-weight: 400; color: #666666; margin: 0 0 1rem 0;">Ejemplos de consultas</p>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        
        examples = [
            ("💰 Pensión", "Mi ex no paga pensión, ¿qué hago?"),
            ("⚖️ Conciliación", "¿Cuánto dura una conciliación?"),
            ("👔 Laboral", "Mi jefe no me paga horas extra")
        ]
        
        for col, (title, example) in zip([col1, col2, col3], examples):
            with col:
                if st.button(title, key=f"example_{title}", use_container_width=True):
                    # Agregar mensaje del usuario directamente
                    current_conv["messages"].append({"role": "user", "content": example})
                    current_conv["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    update_conversation_title(current_conv)
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
    
    # Procesar pregunta del input o de los ejemplos
    question_to_process = None
    
    # Verificar si hay una pregunta del input
    if user_input and user_input.strip() and user_input != st.session_state.last_input:
        question_to_process = user_input
        st.session_state.last_input = user_input
    # Verificar si hay un mensaje pendiente del usuario (de ejemplos)
    elif len(current_conv["messages"]) > 0 and current_conv["messages"][-1]["role"] == "user":
        # Verificar que no tenga respuesta aún
        if len(current_conv["messages"]) == 1 or current_conv["messages"][-2]["role"] != "assistant":
            question_to_process = current_conv["messages"][-1]["content"]
    
    if question_to_process:
        # Si la pregunta no está en el historial, agregarla
        if not (len(current_conv["messages"]) > 0 and current_conv["messages"][-1]["content"] == question_to_process):
            current_conv["messages"].append({"role": "user", "content": question_to_process})
            current_conv["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            update_conversation_title(current_conv)
        
        # Mostrar mensaje del usuario inmediatamente
        st.markdown(
            f'<div class="message user-message">{question_to_process}</div>',
            unsafe_allow_html=True
        )
        
        # Preparar historial para la API
        history = [
            {"role": msg["role"], "content": msg["content"]}
            for msg in current_conv["messages"][:-1]  # Excluir última pregunta
        ]
        
        # Obtener respuesta del API
        with st.spinner("⚖️ Pensando..."):
            response = ask_question(question_to_process, history)
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