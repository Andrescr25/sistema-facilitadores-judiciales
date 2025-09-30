# 🌍 Acceso desde Internet - Chat FJ

## ✅ ngrok ya está configurado!

Tu token de acceso ya está guardado en el sistema.

---

## 🚀 Uso Rápido

### Opción 1: Todo automático
```powershell
.\bin\start_public.ps1
```
Esto inicia el servidor Y el túnel ngrok automáticamente.

### Opción 2: Solo túnel (si el servidor ya está corriendo)
```powershell
.\bin\start_ngrok.ps1
```

---

## 📱 Cómo acceder

1. **Ejecuta** uno de los scripts de arriba
2. **Busca** en la ventana de ngrok una línea como:
   ```
   Forwarding    https://abc123.ngrok-free.app -> http://localhost:8501
   ```
3. **Copia** esa URL (ejemplo: `https://abc123.ngrok-free.app`)
4. **Úsala** en cualquier navegador, móvil o compártela

---

## 🎯 Casos de uso

### Desde tu móvil
- Abre el navegador
- Pega la URL de ngrok
- ¡Listo!

### Compartir con otros
- Envía la URL por WhatsApp/Email
- Cualquiera puede acceder
- Funciona desde cualquier lugar

---

## ⚠️ Importante

- La URL **cambia cada vez** que reinicias ngrok
- La versión gratuita es suficiente para uso normal
- El túnel **solo funciona** mientras ngrok esté corriendo
- Presiona `Ctrl+C` para detener

---

## 🔒 Seguridad

✅ Conexión segura (HTTPS automático)  
✅ Solo quien tenga la URL puede acceder  
✅ No es accesible por Google u otros buscadores  
⚠️ No compartas la URL públicamente si tienes datos sensibles

---

## 📞 Archivos relacionados

- **Scripts:** `bin/start_ngrok.ps1`, `bin/start_public.ps1`
- **ngrok instalado en:** `C:\Users\javar\ngrok.exe`
- **Configuración:** `C:\Users\javar\.ngrok2\ngrok.yml`

---

**Fecha de configuración:** Septiembre 30, 2025  
**Sistema:** Chat FJ v2.0
