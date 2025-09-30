# 🚀 Inicio Rápido - 3 Pasos

## 1️⃣ Instalar Dependencias

```bash
pip install -r requirements.txt
```

## 2️⃣ Configurar Groq API (Opcional pero Recomendado)

1. Obtén tu API Key gratis en: [console.groq.com](https://console.groq.com)
2. Edita `config/config.env`:
   ```env
   GROQ_API_KEY=tu_api_key_aqui
   ```

## 3️⃣ Iniciar el Sistema

```bash
python inicio.py
```

**¡Listo!** Abre http://localhost:8501 y chatea con el bot.

---

## 📝 Comandos Útiles

```bash
# Sistema completo (API + Web)
python inicio.py

# Solo API
python bin/start.py

# Consola
python bin/console.py

# Verificar estado
python bin/status.py

# Tests
python tests/test.py
```

## 🆘 Problemas Comunes

### Error: "Module not found"
```bash
pip install -r requirements.txt
```

### Error: "GROQ_API_KEY not found"
```bash
# Edita config/config.env y agrega tu API key
nano config/config.env
```

### Puerto 8000 o 8501 ocupado
```bash
# Detener procesos Python
# Windows:
taskkill /F /IM python.exe
# Linux/Mac:
killall python
```

---

## ✅ ¡Todo Listo!

El sistema ya está funcionando con:
- ⚡ MockLLM para preguntas comunes (< 1s)
- 🚀 Groq API para preguntas variadas (1-3s)
- 📚 Búsqueda en documentos legales
- 💬 Historial conversacional
- 🎨 Interfaz minimalista tipo ChatGPT

**¿Necesitas más ayuda?** Lee el [README.md](README.md) completo.
