#!/usr/bin/env python3
"""
Interfaz web minimalista para el bot de Facilitadores Judiciales.
Con efecto de escritura tipo ChatGPT.
"""

import streamlit as st
import requests
import time
import os
from typing import Dict, Any

# Configuración de la página
st.set_page_config(
    page_title="Facilitador Judicial IA",
    page_icon="⚖️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Configuración
API_URL = os.getenv("API_URL", "http://localhost:8000")
ASK_ENDPOINT = f"{API_URL}/ask"

# CSS minimalista
st.markdown("""
<style>
    /* Ocultar elementos de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Contenedor principal */
    .main {
        padding-top: 2rem;
        max-width: 800px;
        margin: 0 auto;
    }
    
    /* Título */
    .title {
        text-align: center;
        font-size: 2rem;
        font-weight: 600;
        color: #1a1a1a;
        margin-bottom: 0.5rem;
    }
    
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 0.9rem;
        margin-bottom: 2rem;
    }
    
    /* Mensajes */
    .stChatMessage {
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 12px;
    }
    
    /* Mensaje del usuario */
    [data-testid="stChatMessageContent"] {
        background-color: transparent;
    }
    
    /* Input */
    .stChatInputContainer {
        border-top: 1px solid #e5e5e5;
        padding-top: 1rem;
    }
    
    /* Botón de limpiar */
    .clear-button {
        position: fixed;
        top: 1rem;
        right: 1rem;
        z-index: 999;
    }
    
    /* Ejemplos */
    .example-card {
        background: #f8f9fa;
        border: 1px solid #e5e5e5;
        border-radius: 8px;
        padding: 0.75rem 1rem;
        margin: 0.5rem 0;
        cursor: pointer;
        transition: all 0.2s;
        font-size: 0.9rem;
    }
    
    .example-card:hover {
        background: #e9ecef;
        border-color: #dee2e6;
    }
    
    /* Animación de escritura */
    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0; }
    }
    
    .cursor {
        display: inline-block;
        width: 2px;
        height: 1em;
        background-color: #1a1a1a;
        animation: blink 1s infinite;
        margin-left: 2px;
    }
</style>
""", unsafe_allow_html=True)

def typing_effect(text: str, placeholder):
    """Efecto de escritura palabra por palabra tipo ChatGPT"""
    words = text.split()
    displayed_text = ""
    
    for i, word in enumerate(words):
        displayed_text += word + " "
        # Actualizar el texto con cursor parpadeante
        placeholder.markdown(displayed_text + "▊", unsafe_allow_html=True)
        # Velocidad de escritura ajustable
        time.sleep(0.03)  # 30ms entre palabras
    
    # Mostrar texto final sin cursor
    placeholder.markdown(displayed_text)

def ask_question(question: str, history: list = None) -> Dict[str, Any]:
    """Envía pregunta a la API con historial de conversación"""
    try:
        # Preparar historial en formato API
        api_history = []
        if history:
            for msg in history:
                api_history.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })
        
        payload = {
            "question": question,
            "history": api_history
        }
        
        response = requests.post(
            ASK_ENDPOINT,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            return {
                "answer": "Disculpa, hubo un error. Por favor intenta de nuevo.",
                "sources": []
            }
    except Exception as e:
        return {
            "answer": "No pude conectar con el sistema. Intenta más tarde.",
            "sources": []
        }

def initialize_session():
    """Inicializa el estado de la sesión"""
    if "messages" not in st.session_state:
        st.session_state.messages = []

def display_welcome():
    """Mensaje de bienvenida"""
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <div style="font-size: 3rem; margin-bottom: 1rem;">⚖️</div>
        <h2 style="color: #1a1a1a; margin-bottom: 0.5rem;">Asistente Judicial</h2>
        <p style="color: #666; font-size: 1rem;">Pregúntame sobre pensión alimentaria, derechos laborales, facilitación judicial y más</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Preguntas de ejemplo
    st.markdown("##### 💡 Prueba preguntando:")
    
    examples = [
        "¿Mi ex no paga pensión, qué hago?",
        "Problemas con mi jefe en el trabajo",
        "¿Cómo ser facilitador judicial?",
        "¿Cuánto dura una conciliación?"
    ]
    
    cols = st.columns(2)
    for i, example in enumerate(examples):
        with cols[i % 2]:
            if st.button(example, key=f"ex_{i}", use_container_width=True):
                st.session_state.example_clicked = example
                st.rerun()

def main():
    """Función principal"""
    initialize_session()
    
    # Botón de limpiar chat (solo si hay mensajes)
    if st.session_state.messages:
        col1, col2, col3 = st.columns([4, 1, 4])
        with col2:
            if st.button("🗑️", help="Limpiar chat"):
                st.session_state.messages = []
                st.rerun()
    
    # Título
    st.markdown('<div class="title">⚖️ Facilitador Judicial IA</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Tu asistente legal inteligente</div>', unsafe_allow_html=True)
    
    # Mostrar mensajes existentes
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Mensaje de bienvenida
    if not st.session_state.messages:
        display_welcome()
    
    # Manejar ejemplo clickeado
    if hasattr(st.session_state, 'example_clicked'):
        prompt = st.session_state.example_clicked
        del st.session_state.example_clicked
    else:
        # Input del usuario
        prompt = st.chat_input("Escribe tu pregunta aquí...")
    
    # Procesar pregunta
    if prompt:
        # Agregar mensaje del usuario
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Mostrar mensaje del usuario
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Mostrar respuesta del bot con efecto de escritura
        with st.chat_message("assistant"):
            # Crear placeholder para el efecto de escritura
            message_placeholder = st.empty()
            
            # Indicador de procesamiento
            message_placeholder.markdown("⏳ Pensando...")
            
            # Obtener respuesta con historial (sin incluir el mensaje actual)
            response = ask_question(prompt, history=st.session_state.messages[:-1])
            
            # Mostrar con efecto de escritura
            typing_effect(response["answer"], message_placeholder)
        
        # Guardar respuesta en historial
        st.session_state.messages.append({
            "role": "assistant",
            "content": response["answer"]
        })
        
        st.rerun()

if __name__ == "__main__":
    main()