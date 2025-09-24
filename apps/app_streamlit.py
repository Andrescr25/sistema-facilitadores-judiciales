#!/usr/bin/env python3
"""
Interfaz web para el bot de Facilitadores Judiciales usando Streamlit.
Proporciona una interfaz de chat moderna y fácil de usar.
"""

import streamlit as st
import requests
import json
import time
import os
from datetime import datetime
from typing import List, Dict, Any

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
DOCUMENTS_ENDPOINT = f"{API_URL}/documents"

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
</style>
""", unsafe_allow_html=True)

def check_api_health() -> Dict[str, Any]:
    """
    Verifica el estado de la API.
    """
    try:
        response = requests.get(HEALTH_ENDPOINT, timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            return {"status": "error", "message": f"API error: {response.status_code}"}
    except Exception as e:
        return {"status": "error", "message": f"Connection error: {str(e)}"}

def ask_question(question: str) -> Dict[str, Any]:
    """
    Envía una pregunta a la API y devuelve la respuesta.
    """
    try:
        payload = {"question": question}
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

def get_documents_info() -> Dict[str, Any]:
    """
    Obtiene información sobre los documentos cargados.
    """
    try:
        response = requests.get(DOCUMENTS_ENDPOINT, timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            return {"total_documents": 0, "sample_documents": []}
    except Exception as e:
        return {"total_documents": 0, "sample_documents": []}

def initialize_session_state():
    """
    Inicializa el estado de la sesión.
    """
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "api_status" not in st.session_state:
        st.session_state.api_status = check_api_health()
    
    if "documents_info" not in st.session_state:
        st.session_state.documents_info = get_documents_info()

def display_sidebar():
    """
    Muestra la barra lateral con información del sistema.
    """
    with st.sidebar:
        st.markdown("## 📊 Estado del Sistema")
        
        # Estado de la API
        status = st.session_state.api_status
        if status["status"] == "healthy":
            st.markdown("""
            <div class="status-indicator status-online"></div>
            <strong>API Online</strong>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="status-indicator status-offline"></div>
            <strong>API Offline</strong>
            """, unsafe_allow_html=True)
            st.error(f"Error: {status.get('message', 'Unknown error')}")
        
        st.markdown("---")
        
        # Información de documentos
        docs_info = st.session_state.documents_info
        st.markdown("## 📚 Documentos")
        st.metric("Total de documentos", docs_info.get("total_documents", 0))
        
        if docs_info.get("sample_documents"):
            st.markdown("### Documentos disponibles:")
            for doc in docs_info["sample_documents"][:3]:  # Mostrar solo los primeros 3
                st.markdown(f"• {doc.get('filename', 'Desconocido')}")
        
        st.markdown("---")
        
        # Botones de control
        st.markdown("## 🛠️ Controles")
        
        if st.button("🔄 Actualizar estado", use_container_width=True):
            st.session_state.api_status = check_api_health()
            st.session_state.documents_info = get_documents_info()
            st.rerun()
        
        if st.button("🗑️ Limpiar chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
        
        st.markdown("---")
        
        # Información de la aplicación
        st.markdown("## ℹ️ Información")
        st.markdown("""
        **Bot de Facilitadores Judiciales**
        
        Versión: 1.0.0
        
        Este bot utiliza RAG (Retrieval Augmented Generation) para responder preguntas sobre facilitación judicial basándose en documentos especializados.
        """)

def display_chat_interface():
    """
    Muestra la interfaz principal de chat.
    """
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
        # Agregar mensaje del usuario
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Mostrar mensaje del usuario
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generar respuesta del bot
        with st.chat_message("assistant"):
            with st.spinner("🤔 Procesando tu pregunta..."):
                response = ask_question(prompt)
            
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
    """
    Muestra preguntas de ejemplo.
    """
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
                # Simular click en el input de chat
                st.session_state.example_question = question
                st.rerun()

def main():
    """
    Función principal de la aplicación.
    """
    # Inicializar estado
    initialize_session_state()
    
    # Mostrar sidebar
    display_sidebar()
    
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
