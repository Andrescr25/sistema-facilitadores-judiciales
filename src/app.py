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

# CSS Minimalista y Profesional
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
        --bg-user: #1e40af;
        --bg-assistant: #f3f4f6;
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
    }
    
    .main-header h1 {
        color: white;
        font-size: 1.75rem;
        font-weight: 700;
        margin: 0;
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
    }
    
    /* Chat container - SIN fondo blanco, más fluido */
    .chat-container {
        padding: 1rem 0;
        margin: 0;
        min-height: 400px;
        max-height: 500px;
        overflow-y: auto;
        border: none;
        background: transparent;
    }
    
    /* Mensajes */
    .message {
        margin: 0.75rem 0;
        padding: 0.875rem 1rem;
        border-radius: 1rem;
        max-width: 75%;
        line-height: 1.6;
        font-size: 0.95rem;
        animation: fadeIn 0.3s ease-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(5px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .user-message {
        background: var(--bg-user);
        color: white;
        margin-left: auto;
        border-bottom-right-radius: 0.25rem;
    }
    
    .assistant-message {
        background: var(--bg-assistant);
        color: var(--text-dark);
        margin-right: auto;
        border-bottom-left-radius: 0.25rem;
    }
    
    /* Input section */
    .input-section {
        margin: 2rem 0 1rem 0;
        padding-top: 1rem;
        border-top: 1px solid var(--border);
    }
    
    .stTextInput input {
        border: 2px solid var(--border);
        border-radius: 0.75rem;
        padding: 0.875rem 1rem;
        font-size: 0.95rem;
        transition: all 0.2s;
    }
    
    .stTextInput input:focus {
        border-color: var(--primary-light);
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
        outline: none;
    }
    
    /* Botones */
    .stButton button {
        background: var(--primary);
        color: white;
        border: none;
        padding: 0.625rem 1.25rem;
        border-radius: 0.5rem;
        font-weight: 500;
        font-size: 0.875rem;
        transition: all 0.2s;
        width: 100%;
    }
    
    .stButton button:hover {
        background: var(--primary-light);
        transform: translateY(-1px);
    }
    
    /* Footer con disclaimer */
    .footer-disclaimer {
        background: #fef3c7;
        border-top: 2px solid #fcd34d;
        padding: 1rem;
        margin: 2rem -4rem -2rem -4rem;
        text-align: center;
        font-size: 0.875rem;
        color: #92400e;
    }
    
    .footer-disclaimer strong {
        color: #78350f;
    }
    
    /* Loading */
    .stSpinner > div {
        border-top-color: var(--primary) !important;
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
        
        .main-header h1 {
            font-size: 1.5rem;
        }
        
        .message {
            max-width: 85%;
        }
        
        .main .block-container {
            padding: 1.5rem 1rem 1rem 1rem;
        }
        
        .footer-disclaimer {
            margin: 2rem -1rem -1.5rem -1rem;
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
        user_input = st.text_input(
            "Escribe tu pregunta...",
            key="user_input",
            label_visibility="collapsed",
            placeholder="Ejemplo: ¿Cómo solicito pensión alimentaria?"
        )
    
    with col2:
        if st.button("🗑️ Limpiar", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    
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
        with st.spinner("⚖️ Escribiendo..."):
            response = ask_question(user_input, history)
            answer = response.get("answer", "No se obtuvo respuesta")
        
        # Agregar respuesta
        st.session_state.messages.append({"role": "assistant", "content": answer})
        
        st.rerun()
    
    # Footer con disclaimer
    st.markdown("""
    <div class="footer-disclaimer">
        <strong>⚠️ Importante:</strong> Este chat es para orientación general. La información puede contener errores. 
        Verifica siempre con fuentes oficiales o profesionales del derecho.
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()