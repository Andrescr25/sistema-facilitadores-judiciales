# 🔒 Guía de Seguridad

## ⚠️ Nunca Subas Secretos a Git

Este proyecto usa **API keys** y otros secretos que **NUNCA deben subirse** a GitHub.

## 📝 Archivos Protegidos

Los siguientes archivos están en `.gitignore` y **nunca se suben a git**:

```
.env
.env.local
config/config.env
```

## ✅ Configuración Correcta

### 1. Archivo Local (Tu Computadora)
```bash
config/config.env     # ← Tu API key REAL está aquí
                      # ← Este archivo NO se sube a git
                      # ← Solo existe en tu computadora
```

### 2. Archivo de Ejemplo (GitHub)
```bash
config/config.env.example  # ← Ejemplo público sin secretos
                           # ← Este SÍ está en git
                           # ← Otros lo usan como plantilla
```

## 🚀 Setup Inicial

Cuando clones este proyecto:

```bash
# 1. Copia el archivo de ejemplo
cp config/config.env.example config/config.env

# 2. Edita y agrega tu API key REAL
nano config/config.env

# 3. ¡Listo! config.env ya no se subirá a git
```

## 🔐 Obtener API Key de Groq (GRATIS)

1. Ve a [console.groq.com](https://console.groq.com)
2. Crea una cuenta (gratis)
3. Ve a "API Keys"
4. Crea una nueva key
5. Cópiala y pégala en tu `config/config.env`

## ⚠️ Si Expusiste una API Key

Si accidentalmente subiste una API key a git:

1. **Revoca la key inmediatamente** en console.groq.com
2. Crea una nueva key
3. Actualiza tu `config/config.env` local
4. **Nunca uses la key expuesta de nuevo**

## ✅ Verificar Protección

Para verificar que tus secretos están protegidos:

```bash
# Esto NO debe mostrar config/config.env
git status

# Si lo muestra, agregalo a .gitignore
echo "config/config.env" >> .gitignore
```

## 📚 Más Información

- [GitHub Secret Scanning](https://docs.github.com/en/code-security/secret-scanning)
- [Groq API Docs](https://console.groq.com/docs)
- [Best Practices for API Keys](https://cloud.google.com/docs/authentication/api-keys)
