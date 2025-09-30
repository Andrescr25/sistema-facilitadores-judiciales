# 🌍 Acceso desde Internet - Chat FJ

## ⚡ Guía Rápida (3 pasos)

### 1️⃣ Registrarse en ngrok (GRATIS)

1. Ve a: https://dashboard.ngrok.com/signup
2. Regístrate con tu email (toma 1 minuto)
3. Inicia sesión

### 2️⃣ Configurar ngrok (SOLO UNA VEZ)

1. Ve a: https://dashboard.ngrok.com/get-started/your-authtoken
2. Copia tu **Authtoken** (algo como: `2abc...xyz`)
3. En la terminal, ejecuta:
   ```powershell
   cd C:\Users\javar
   .\ngrok.exe config add-authtoken TU_TOKEN_AQUI
   ```
   *(Reemplaza `TU_TOKEN_AQUI` con tu token real)*

### 3️⃣ Iniciar el túnel

**Opción A - Script automático (FÁCIL):**
```powershell
.\start_ngrok.ps1
```

**Opción B - Comando manual:**
```powershell
cd C:\Users\javar
.\ngrok.exe http 8501
```

---

## 📱 Usar desde tu móvil / otro lugar

Una vez que inicies el túnel, verás algo como:

```
Forwarding    https://abc123.ngrok-free.app -> http://localhost:8501
```

**Esa URL** (`https://abc123.ngrok-free.app`) es tu **enlace público**.

✅ **Cópiala y ábrela en cualquier navegador** (móvil, tablet, otra PC)  
✅ Funciona desde **cualquier lugar con internet**  
✅ Es **segura** (HTTPS automático)

---

## 🎯 Flujo completo

1. **Terminal 1:** Ejecuta el servidor
   ```powershell
   python inicio.py
   ```

2. **Terminal 2:** Ejecuta ngrok
   ```powershell
   .\start_ngrok.ps1
   ```

3. **Resultado:** Obtienes una URL pública como:
   ```
   https://abc123.ngrok-free.app
   ```

4. **Comparte** esa URL con quien quieras (móvil, amigos, etc.)

---

## ⚠️ Limitaciones de la versión gratuita

- **Sesión temporal**: La URL cambia cada vez que reinicias ngrok
- **Sin dominio personalizado**: URL aleatoria tipo `abc123.ngrok-free.app`
- **Velocidad**: Puede ser más lenta que acceso local
- **Uso justo**: Límites razonables de tráfico

**Para uso permanente:** Considera la versión paga de ngrok o Cloudflare Tunnel.

---

## 🔒 Seguridad

✅ **Seguro:** ngrok usa HTTPS automáticamente  
✅ **Privado:** Solo quien tenga la URL puede acceder  
✅ **Temporal:** La URL expira cuando cierras ngrok  
⚠️ **No compartas la URL públicamente** si tiene datos sensibles

---

## 🆘 Solución de problemas

### ❌ "ngrok not found"
**Solución:** Ejecuta `.\setup_ngrok.ps1` primero

### ❌ "ERR_NGROK_108"
**Solución:** Necesitas configurar tu authtoken (paso 2)

### ❌ "Failed to complete tunnel connection"
**Solución:** 
1. Verifica que el servidor esté corriendo (`python inicio.py`)
2. Asegúrate de estar usando el puerto correcto (8501)

### ❌ La URL no carga
**Solución:** 
1. Espera 5-10 segundos después de iniciar ngrok
2. Verifica que veas "Session Status: online" en ngrok
3. Prueba la URL en modo incógnito

---

## 💡 Alternativas

Si ngrok no funciona o necesitas algo permanente:

### Cloudflare Tunnel (Gratis, Permanente)
```bash
# Instalar cloudflared
# https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/
cloudflared tunnel --url http://localhost:8501
```

### Serveo (Sin registro, menos estable)
```bash
ssh -R 80:localhost:8501 serveo.net
```

---

## 📞 Información técnica

- **Puerto local:** 8501 (Streamlit)
- **Protocolo:** HTTP → HTTPS (automático por ngrok)
- **ngrok instalado en:** `C:\Users\javar\ngrok.exe`
- **Config ngrok:** `C:\Users\javar\.ngrok2\ngrok.yml`

---

**Fecha de configuración:** Septiembre 30, 2025  
**Sistema:** Chat FJ v2.0  
**Método:** ngrok tunnel
