#!/usr/bin/env python3
"""
Chat FJ - Servicio Nacional de Facilitadoras y Facilitadores Judiciales
Interfaz web profesional con Streamlit
"""

import streamlit as st
import requests
import time
from typing import List, Dict

# Configuración de la página
st.set_page_config(
    page_title="Chat FJ | Poder Judicial Costa Rica",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS Profesional y Moderno
st.markdown("""
<style>
    /* Importar fuente profesional */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Variables de color corporativas */
    :root {
        --primary-color: #1e40af;
        --secondary-color: #3b82f6;
        --accent-color: #60a5fa;
        --success-color: #10b981;
        --warning-color: #f59e0b;
        --text-dark: #1f2937;
        --text-light: #6b7280;
        --bg-light: #f9fafb;
        --border-color: #e5e7eb;
    }
    
    /* Reset y base */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    /* Ocultar elementos de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Header corporativo */
    .main-header {
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
        padding: 2rem 2.5rem;
        border-radius: 0;
        margin: -6rem -4rem 2rem -4rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    .header-content {
        max-width: 1200px;
        margin: 0 auto;
    }
    
    .logo-section {
        display: flex;
        align-items: center;
        gap: 1.5rem;
        margin-bottom: 0.75rem;
    }
    
    .logo {
        font-size: 3rem;
        filter: drop-shadow(0 2px 4px rgba(0,0,0,0.1));
    }
    
    .brand-text h1 {
        color: white;
        font-size: 2rem;
        font-weight: 700;
        margin: 0;
        line-height: 1.2;
    }
    
    .brand-text p {
        color: rgba(255, 255, 255, 0.9);
        font-size: 0.95rem;
        margin: 0.25rem 0 0 0;
        font-weight: 400;
    }
    
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        padding: 0.5rem 1rem;
        border-radius: 2rem;
        color: white;
        font-size: 0.875rem;
        font-weight: 500;
        margin-top: 0.75rem;
    }
    
    .status-dot {
        width: 8px;
        height: 8px;
        background: #10b981;
        border-radius: 50%;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    /* Contenedor principal */
    .main .block-container {
        max-width: 1200px;
        padding: 2rem 3rem 3rem 3rem;
    }
    
    /* Chat container */
    .chat-container {
        background: white;
        border-radius: 1rem;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
        padding: 1.5rem;
        margin: 1.5rem 0;
        min-height: 500px;
        max-height: 600px;
        overflow-y: auto;
    }
    
    /* Mensajes */
    .message {
        margin: 1rem 0;
        padding: 1rem 1.25rem;
        border-radius: 1rem;
        max-width: 75%;
        animation: slideIn 0.3s ease-out;
    }
    
    @keyframes slideIn {
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
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
        color: white;
        margin-left: auto;
        border-bottom-right-radius: 0.25rem;
    }
    
    .assistant-message {
        background: #f9fafb;
        color: #1f2937;
        border: 1px solid #e5e7eb;
        margin-right: auto;
        border-bottom-left-radius: 0.25rem;
    }
    
    .message-header {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 0.5rem;
        font-size: 0.875rem;
        font-weight: 600;
        opacity: 0.9;
    }
    
    .message-content {
        line-height: 1.6;
        font-size: 0.95rem;
    }
    
    /* Input section */
    .input-section {
        background: white;
        border-radius: 1rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        padding: 1.5rem;
        margin: 2rem 0;
    }
    
    /* Botones de ejemplo */
    .example-questions {
        display: flex;
        gap: 0.75rem;
        flex-wrap: wrap;
        margin: 1.5rem 0;
    }
    
    .example-btn {
        background: white;
        border: 2px solid #e5e7eb;
        padding: 0.625rem 1rem;
        border-radius: 2rem;
        font-size: 0.875rem;
        color: #4b5563;
        cursor: pointer;
        transition: all 0.2s;
        font-weight: 500;
    }
    
    .example-btn:hover {
        background: #f9fafb;
        border-color: #3b82f6;
        color: #1e40af;
        transform: translateY(-1px);
    }
    
    /* Botón limpiar */
    .stButton button {
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
        color: white;
        border: none;
        padding: 0.625rem 1.5rem;
        border-radius: 0.5rem;
        font-weight: 600;
        font-size: 0.875rem;
        cursor: pointer;
        transition: all 0.2s;
        width: 100%;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(30, 64, 175, 0.3);
    }
    
    /* Input de texto */
    .stTextInput input {
        border: 2px solid #e5e7eb;
        border-radius: 0.75rem;
        padding: 0.875rem 1rem;
        font-size: 0.95rem;
        transition: all 0.2s;
    }
    
    .stTextInput input:focus {
        border-color: #3b82f6;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
    }
    
    /* Footer corporativo */
    .footer {
        text-align: center;
        padding: 2rem;
        margin-top: 3rem;
        color: #6b7280;
        font-size: 0.875rem;
        border-top: 1px solid #e5e7eb;
    }
    
    .footer-links {
        display: flex;
        justify-content: center;
        gap: 2rem;
        margin-top: 1rem;
    }
    
    .footer-link {
        color: #3b82f6;
        text-decoration: none;
        font-weight: 500;
    }
    
    .footer-link:hover {
        color: #1e40af;
    }
    
    /* Typing animation */
    .typing-indicator {
        display: flex;
        gap: 0.25rem;
        padding: 1rem;
    }
    
    .typing-dot {
        width: 8px;
        height: 8px;
        background: #9ca3af;
        border-radius: 50%;
        animation: typing 1.4s infinite;
    }
    
    .typing-dot:nth-child(2) {
        animation-delay: 0.2s;
    }
    
    .typing-dot:nth-child(3) {
        animation-delay: 0.4s;
    }
    
    @keyframes typing {
        0%, 60%, 100% {
            transform: translateY(0);
            opacity: 0.7;
        }
        30% {
            transform: translateY(-10px);
            opacity: 1;
        }
    }
    
    /* Scroll suave */
    .chat-container {
        scroll-behavior: smooth;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .main-header {
            padding: 1.5rem 1rem;
            margin: -4rem -1rem 1.5rem -1rem;
        }
        
        .brand-text h1 {
            font-size: 1.5rem;
        }
        
        .message {
            max-width: 90%;
        }
        
        .example-questions {
            flex-direction: column;
        }
    }
</style>
""", unsafe_allow_html=True)

# Header corporativo
st.markdown("""
<div class="main-header">
    <div class="header-content">
        <div class="logo-section">
            <div class="logo">⚖️</div>
            <div class="brand-text">
                <h1>Chat FJ</h1>
                <p>Servicio Nacional de Facilitadoras y Facilitadores Judiciales</p>
            </div>
        </div>
        <div class="status-badge">
            <div class="status-dot"></div>
            <span>Sistema en línea | Poder Judicial Costa Rica</span>
        </div>
    </div>
</div>
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

def typing_effect(text: str, container):
    """Efecto de escritura tipo ChatGPT."""
    words = text.split()
    displayed_text = ""
    
    for i, word in enumerate(words):
        displayed_text += word + " "
        container.markdown(
            f'<div class="message assistant-message">'
            f'<div class="message-header">⚖️ Chat FJ</div>'
            f'<div class="message-content">{displayed_text}▌</div>'
            f'</div>',
            unsafe_allow_html=True
        )
        time.sleep(0.03)
    
    # Mostrar texto final sin cursor
    container.markdown(
        f'<div class="message assistant-message">'
        f'<div class="message-header">⚖️ Chat FJ</div>'
        f'<div class="message-content">{text}</div>'
        f'</div>',
        unsafe_allow_html=True
    )

def main():
    """Aplicación principal."""
    
    # Inicializar estado de sesión
    if "messages" not in st.session_state:
        st.session_state.messages = []
        # Mensaje de bienvenida
        welcome_msg = {
            "role": "assistant",
            "content": "¡Hola! 👋 Soy **Chat FJ**, tu asistente virtual del Servicio Nacional de Facilitadoras y Facilitadores Judiciales de Costa Rica.\n\nEstoy aquí para ayudarte con información sobre procesos legales, conciliación, pensión alimentaria y más. ¿En qué puedo asistirte hoy?"
        }
        st.session_state.messages.append(welcome_msg)
    
    # Preguntas de ejemplo
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0 1rem 0;">
        <h3 style="color: #1f2937; font-weight: 600; margin-bottom: 0.5rem;">💬 Pregunta al Chat FJ</h3>
        <p style="color: #6b7280; font-size: 0.95rem;">Selecciona una pregunta frecuente o escribe la tuya:</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Botones de ejemplo en columnas
    col1, col2, col3 = st.columns(3)
    
    example_questions = [
        "¿Cómo solicito pensión alimentaria?",
        "¿Cuánto dura una conciliación?",
        "¿Cómo ser facilitadora o facilitador?"
    ]
    
    for col, question in zip([col1, col2, col3], example_questions):
        if col.button(f"💡 {question}", key=f"ex_{question}", use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": question})
            st.rerun()
    
    # Contenedor de chat
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Mostrar mensajes
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(
                f'<div class="message user-message">'
                f'<div class="message-header">👤 Tú</div>'
                f'<div class="message-content">{message["content"]}</div>'
                f'</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f'<div class="message assistant-message">'
                f'<div class="message-header">⚖️ Chat FJ</div>'
                f'<div class="message-content">{message["content"]}</div>'
                f'</div>',
                unsafe_allow_html=True
            )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Input de texto
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([5, 1])
    
    with col1:
        user_input = st.text_input(
            "Escribe tu pregunta aquí...",
            key="user_input",
            label_visibility="collapsed",
            placeholder="Ejemplo: ¿Cómo inicio un proceso de conciliación?"
        )
    
    with col2:
        if st.button("🗑️ Limpiar", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Procesar pregunta
    if user_input:
        # Agregar mensaje del usuario
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Preparar historial para la API
        history = [
            {"role": msg["role"], "content": msg["content"]}
            for msg in st.session_state.messages[1:-1]  # Excluir bienvenida y última pregunta
        ]
        
        # Obtener respuesta
        with st.spinner("⚖️ Chat FJ está escribiendo..."):
            response = ask_question(user_input, history)
            answer = response.get("answer", "No se obtuvo respuesta")
        
        # Agregar respuesta
        st.session_state.messages.append({"role": "assistant", "content": answer})
        
        st.rerun()
    
    # Footer corporativo
    st.markdown("""
    <div class="footer">
        <p><strong>Servicio Nacional de Facilitadoras y Facilitadores Judiciales</strong></p>
        <p>Poder Judicial de Costa Rica | Sistema de Resolución Alterna de Conflictos</p>
        <div class="footer-links">
            <a href="https://www.poder-judicial.go.cr" class="footer-link" target="_blank">🌐 Poder Judicial</a>
            <a href="http://localhost:8000/docs" class="footer-link" target="_blank">📚 API Docs</a>
            <a href="#" class="footer-link">📞 Contacto: 2295-3000</a>
        </div>
        <p style="margin-top: 1rem; font-size: 0.8rem; opacity: 0.7;">
            © 2025 Poder Judicial de Costa Rica. Todos los derechos reservados.
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()