#!/usr/bin/env python3
"""
Chat FJ - Servicio Nacional de Facilitadoras y Facilitadores Judiciales
Interfaz web minimalista con Streamlit
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

# CSS Moderno con burbujas mejoradas
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
    }
    
    /* Reset */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    /* Ocultar elementos de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Header minimalista */
    .main-header {
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
        padding: 2rem;
        margin: -6rem -4rem 2rem -4rem;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .main-header h1 {
        color: white;
        font-size: 1.75rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.02em;
    }
    
    .main-header p {
        color: rgba(255, 255, 255, 0.9);
        font-size: 0.9rem;
        margin: 0.5rem 0 0 0;
        font-weight: 400;
    }
    
    /* Contenedor principal */
    .main .block-container {
        max-width: 900px;
        padding: 2rem 2rem 1rem 2rem;
        background: #fafafa;
    }
    
    /* Chat container */
    .chat-container {
        padding: 1rem 0 2rem 0;
        margin: 0;
        min-height: 400px;
        max-height: 500px;
        overflow-y: auto;
        border: none;
        background: transparent;
    }
    
    /* Mensajes mejorados estilo WhatsApp/ChatGPT */
    .message {
        margin: 0.75rem 0;
        padding: 0.875rem 1.125rem;
        border-radius: 1.125rem;
        max-width: 70%;
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
    
    /* Input section */
    .input-section {
        margin: 2rem 0 1rem 0;
        padding-top: 1.5rem;
        border-top: 1px solid var(--border);
    }
    
    .stTextInput input {
        border: 1px solid var(--border);
        border-radius: 1.5rem;
        padding: 0.875rem 1.125rem;
        font-size: 0.95rem;
        transition: all 0.2s;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    }
    
    .stTextInput input:focus {
        border-color: var(--primary-light);
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
        outline: none;
    }
    
    /* Botones */
    .stButton button {
        background: white;
        color: var(--text-dark);
        border: 1px solid var(--border);
        padding: 0.625rem 1rem;
        border-radius: 0.75rem;
        font-weight: 500;
        font-size: 0.875rem;
        transition: all 0.2s;
        width: 100%;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    }
    
    .stButton button:hover {
        background: #f9fafb;
        border-color: var(--primary-light);
        transform: translateY(-1px);
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Footer estilo ChatGPT */
    .footer-disclaimer {
        background: transparent;
        border-top: 1px solid #e5e7eb;
        padding: 1rem 2rem;
        margin: 2rem -4rem -2rem -4rem;
        text-align: center;
        font-size: 0.75rem;
        color: #6b7280;
    }
    
    .footer-disclaimer a {
        color: #6b7280;
        text-decoration: underline;
        transition: color 0.2s;
    }
    
    .footer-disclaimer a:hover {
        color: #374151;
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
    
    /* Responsive */
    @media (max-width: 768px) {
        .main-header {
            padding: 1.5rem 1rem;
            margin: -4rem -1rem 1.5rem -1rem;
        }
        
        .main-header h1 {
            font-size: 1.5rem;
        }
        
        .message {
            max-width: 80%;
        }
        
        .main .block-container {
            padding: 1.5rem 1rem 1rem 1rem;
        }
        
        .footer-disclaimer {
            margin: 2rem -1rem -1.5rem -1rem;
            padding: 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Header minimalista
st.markdown("""
<div class="main-header">
    <h1>⚖️ Chat FJ</h1>
    <p>Servicio Nacional de Facilitadoras y Facilitadores Judiciales</p>
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

def main():
    """Aplicación principal."""
    
    # Inicializar estado de sesión
    if "messages" not in st.session_state:
        st.session_state.messages = []
        # Mensaje de bienvenida
        welcome_msg = {
            "role": "assistant",
            "content": "Hola, soy Chat FJ. ¿En qué puedo ayudarte hoy?"
        }
        st.session_state.messages.append(welcome_msg)
    
    # Almacenar el último input procesado
    if "last_input" not in st.session_state:
        st.session_state.last_input = ""
    
    # Contenedor de chat
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Mostrar mensajes
    for message in st.session_state.messages:
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
    
    # Input de texto
    st.markdown('<div class="input-section"></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([5, 1])
    
    with col1:
        # Usar key única con el contador de mensajes para forzar reset
        input_key = f"user_input_{len(st.session_state.messages)}"
        user_input = st.text_input(
            "Escribe tu pregunta...",
            key=input_key,
            label_visibility="collapsed",
            placeholder="Envía un mensaje a Chat FJ..."
        )
    
    with col2:
        if st.button("🗑️ Limpiar", use_container_width=True):
            st.session_state.messages = []
            st.session_state.last_input = ""
            st.rerun()
    
    # Procesar pregunta SOLO si es diferente al último input procesado
    if user_input and user_input.strip() and user_input != st.session_state.last_input:
        # Guardar este input como procesado
        st.session_state.last_input = user_input
        
        # Agregar mensaje del usuario
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Mostrar mensaje del usuario inmediatamente
        st.markdown(
            f'<div class="message user-message">{user_input}</div>',
            unsafe_allow_html=True
        )
        
        # Preparar historial para la API
        history = [
            {"role": msg["role"], "content": msg["content"]}
            for msg in st.session_state.messages[1:-1]  # Excluir bienvenida y última pregunta
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
        st.session_state.messages.append({"role": "assistant", "content": answer})
        
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