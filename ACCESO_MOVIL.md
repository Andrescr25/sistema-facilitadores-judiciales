# 📱 Acceso desde Móvil - Chat FJ

## 🌐 Dirección para acceder desde tu móvil:

### **Interfaz Web:**
```
http://192.168.0.16:8501
```

## 📋 Pasos para conectar:

1. **Asegúrate de estar en la misma red WiFi** que esta computadora
2. **Abre el navegador** en tu móvil (Chrome, Safari, Firefox, etc.)
3. **Escribe la dirección:**
   ```
   http://192.168.0.16:8501
   ```
4. **¡Listo!** Deberías ver Chat FJ funcionando

---

## 🔍 Código QR para acceso rápido:

Escanea este QR con tu cámara:

```
█████████████████████████████████████
██ ▄▄▄▄▄ █▀ ▀ █ ▀█▄█▀ ██▀▄█ ▄▄▄▄▄ ██
██ █   █ █ █▀██▄▀ ▄▀ ▄▄▀▄██ █   █ ██
██ █▄▄▄█ █▀ ▄ ▄ ▄ ███▀█▀▀▄█ █▄▄▄█ ██
██▄▄▄▄▄▄▄█▄▀ █ █ ▀▄▀ █▄█ █▄▄▄▄▄▄▄██
██ ▄▄▀▀▀▄▄▀▄ █▀ █▀▄██  ▀▀ ▄ ▀█▄█▀██
██▀▀█▀▄ ▄▀▄▄█▀▀█▀█▀▀█▀▀ █▀▀█▄ ▀  ██
██ █▀█▀▀▄▄ ▄█▀ ▄▄▄█  █▄▄▀ ▀▄█▄█▄ ██
██▄█▄█▄▄▄█▀▀▄▄▀▄█▀▄ ▀█ ▄▄▄ ▀   ▄▀██
██ ▄▄▄▄▄ █▄▀▄ ▄█ ▀▄▀█ █▄█ ▀▄█▄ ▄▄██
██ █   █ █ ▄  ▀▄██▄▀  ▄▄  ▀▄▀▀█ ▄██
██ █▄▄▄█ █ ██▄█▀▄▄▄▀▄▀█▄▄█▀ ▄▄▄█ ██
██▄▄▄▄▄▄▄█▄█▄▄▄█▄██▄▄█▄▄███▄▄▄█▄▄██
█████████████████████████████████████
```

O genera uno en: https://www.qr-code-generator.com/ con la URL:
`http://192.168.0.16:8501`

---

## ⚠️ Solución de problemas:

### ❌ No carga / Timeout
- ✅ Verifica que ambos dispositivos estén en la **misma red WiFi**
- ✅ Asegúrate de que el servidor esté corriendo en la PC
- ✅ Si persiste, desactiva temporalmente el **Firewall de Windows**:
  - `Windows Security → Firewall → Desactivar`

### ❌ "Sitio no disponible"
- ✅ Verifica que el servidor esté corriendo: `python inicio.py`
- ✅ Confirma la IP ejecutando: `ipconfig` en la terminal

### ❌ Se conecta pero va muy lento
- ✅ Acércate al router WiFi
- ✅ Verifica la señal en ambos dispositivos
- ✅ Cierra otras aplicaciones que usen internet

---

## 🔒 Nota de Seguridad

Esta configuración **solo permite acceso desde tu red local**. No es accesible desde internet (seguro para uso interno).

---

## 📞 Información adicional

- **API (para desarrolladores):** `http://192.168.0.16:8000`
- **Documentación API:** `http://192.168.0.16:8000/docs`
- **Puerto Streamlit:** 8501
- **Puerto API:** 8000

---

**Fecha de configuración:** Septiembre 30, 2025  
**IP Local:** 192.168.0.16  
**Sistema:** Chat FJ v2.0
