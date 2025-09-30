# 📱 Acceso desde Móvil (Red Local) - Chat FJ

## 🌐 Dirección para acceder desde tu móvil

### **En la misma red WiFi:**
```
http://192.168.0.16:8501
```

---

## 📋 Pasos para conectar

1. **Asegúrate** de que tu móvil esté en la **misma red WiFi** que la PC
2. **Abre** el navegador en tu móvil (Chrome, Safari, Firefox)
3. **Escribe** en la barra de direcciones:
   ```
   http://192.168.0.16:8501
   ```
4. **¡Listo!** Deberías ver Chat FJ funcionando

---

## 🔍 Código QR para acceso rápido

Genera un QR en: https://www.qr-code-generator.com/

Con esta URL: `http://192.168.0.16:8501`

Luego escanéalo con la cámara de tu móvil.

---

## ⚠️ Solución de problemas

### ❌ No carga / Timeout
- ✅ Verifica que **ambos dispositivos** estén en la **misma red WiFi**
- ✅ Asegúrate de que el servidor esté corriendo (`python inicio.py`)
- ✅ Si persiste, desactiva temporalmente el **Firewall de Windows**

### ❌ "Sitio no disponible"
- ✅ Confirma que el servidor esté corriendo
- ✅ Verifica la IP ejecutando `ipconfig` en la terminal de la PC

### ❌ Se conecta pero va muy lento
- ✅ Acércate al router WiFi
- ✅ Cierra otras aplicaciones que usen internet

---

## 💡 Nota

Este método **solo funciona** si ambos dispositivos están en la **misma red WiFi**.

Si necesitas acceder desde **otra red** o **internet**, usa ngrok:
- Ver: `docs/ACCESO_INTERNET.md`
- Ejecutar: `.\bin\start_public.ps1`

---

## 🔒 Seguridad

✅ **Seguro:** Solo accesible en tu red local  
✅ **Privado:** No es accesible desde internet  
✅ **Rápido:** Conexión directa sin intermediarios

---

**IP Local:** 192.168.0.16  
**Puerto:** 8501  
**Sistema:** Chat FJ v2.0
