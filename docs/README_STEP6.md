# PASO 6 - Autenticación básica y seguridad

## Objetivo
Implementar un sistema de autenticación básico con tokens y medidas de seguridad para proteger la API del bot de facilitadores judiciales.

## Archivos generados
- `app/security.py` - Módulo de seguridad y autenticación
- `app/api.py` - API actualizada con autenticación
- `README_STEP6.md` - Este archivo de instrucciones

## Características de seguridad implementadas

### Autenticación:
- ✅ Tokens JWT-like con expiración configurable
- ✅ Tokens de desarrollo para testing
- ✅ Validación de tokens en cada request
- ✅ Rate limiting por IP (60 requests/minuto por defecto)
- ✅ Logging de eventos de seguridad

### Autorización:
- ✅ Sistema de roles (admin, facilitador, user)
- ✅ Permisos granulares por endpoint
- ✅ Verificación de permisos en tiempo real

### Endpoints de seguridad:
- **`POST /auth/login`** - Generar token de autenticación
- **`POST /auth/logout`** - Revocar token
- **`GET /auth/me`** - Información del usuario actual
- **`GET /auth/dev-tokens`** - Tokens de desarrollo
- **`GET /security/stats`** - Estadísticas de seguridad
- **`POST /security/cleanup`** - Limpiar datos expirados

## Configuración de seguridad

### Variables de entorno:
```bash
# Habilitar/deshabilitar autenticación
ENABLE_AUTH=true

# Configuración de tokens
SECRET_KEY=tu-clave-secreta-muy-segura
TOKEN_EXPIRY_HOURS=24

# Rate limiting
MAX_REQUESTS_PER_MINUTE=60
```

### Roles y permisos:

**Admin:**
- ✅ read, write, delete
- ✅ manage_users, view_logs

**Facilitador:**
- ✅ read, write
- ❌ delete, manage_users, view_logs

**User:**
- ✅ read
- ❌ write, delete, manage_users, view_logs

## Instrucciones de uso

### 1. Configurar variables de entorno
```bash
# Crear archivo .env con configuración de seguridad
cat > .env << EOF
ENABLE_AUTH=true
SECRET_KEY=$(python -c "import secrets; print(secrets.token_urlsafe(32))")
TOKEN_EXPIRY_HOURS=24
MAX_REQUESTS_PER_MINUTE=60
EOF

# Cargar variables
source .env
```

### 2. Iniciar API con autenticación
```bash
source venv/bin/activate
python app/api.py
```

### 3. Obtener token de autenticación
```bash
# Generar token para usuario
curl -X POST "http://localhost:8000/auth/login?user_id=admin&role=admin"

# Respuesta:
{
  "access_token": "abc123...",
  "token_type": "bearer",
  "user_id": "admin",
  "role": "admin",
  "expires_in": 86400
}
```

### 4. Usar token en requests
```bash
# Hacer consulta con autenticación
curl -X POST "http://localhost:8000/ask" \
  -H "Authorization: Bearer abc123..." \
  -H "Content-Type: application/json" \
  -d '{"question": "¿Cuáles son los requisitos para ser facilitador?"}'
```

## Ejemplos de uso

### 1. Login y obtención de token
```bash
# Login como administrador
curl -X POST "http://localhost:8000/auth/login?user_id=admin&role=admin"

# Login como facilitador
curl -X POST "http://localhost:8000/auth/login?user_id=facilitador1&role=facilitador"

# Login como usuario regular
curl -X POST "http://localhost:8000/auth/login?user_id=usuario1&role=user"
```

### 2. Consultas autenticadas
```bash
# Token obtenido del login
TOKEN="tu-token-aqui"

# Hacer consulta
curl -X POST "http://localhost:8000/ask" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"question": "¿Cuánto dura el procedimiento?"}'
```

### 3. Verificar información del usuario
```bash
curl -H "Authorization: Bearer $TOKEN" \
  "http://localhost:8000/auth/me"
```

### 4. Obtener estadísticas de seguridad (solo admin)
```bash
curl -H "Authorization: Bearer $TOKEN" \
  "http://localhost:8000/security/stats"
```

## Modo desarrollo sin autenticación

Para desarrollo local, puedes deshabilitar la autenticación:

```bash
# Deshabilitar autenticación
export ENABLE_AUTH=false

# Iniciar API
python app/api.py

# Ahora todos los endpoints funcionan sin token
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "¿Cuáles son los requisitos?"}'
```

## Tokens de desarrollo

Cuando `ENABLE_AUTH=false`, puedes obtener tokens predefinidos:

```bash
curl "http://localhost:8000/auth/dev-tokens"

# Respuesta:
{
  "tokens": {
    "admin": "dev-admin-token-12345",
    "user": "dev-user-token-67890",
    "facilitador": "dev-facilitador-token-abcde"
  },
  "note": "Estos tokens son solo para desarrollo. No usar en producción."
}
```

## Solución de problemas

### Error: "Token de autenticación requerido"
```bash
# Verificar que el token esté en el header Authorization
curl -H "Authorization: Bearer tu-token" "http://localhost:8000/ask"
```

### Error: "Permiso insuficiente"
```bash
# Verificar que el usuario tenga el rol correcto
curl -H "Authorization: Bearer $TOKEN" "http://localhost:8000/auth/me"
```

### Error: "Demasiadas solicitudes"
```bash
# Esperar un minuto o aumentar MAX_REQUESTS_PER_MINUTE
export MAX_REQUESTS_PER_MINUTE=120
```

### Error: "Token expirado"
```bash
# Generar nuevo token
curl -X POST "http://localhost:8000/auth/login?user_id=usuario&role=user"
```

## Configuración para producción

### 1. Variables de entorno seguras
```bash
# Generar clave secreta fuerte
SECRET_KEY=$(python -c "import secrets; print(secrets.token_urlsafe(64))")

# Configuración de producción
ENABLE_AUTH=true
TOKEN_EXPIRY_HOURS=8  # Tokens más cortos
MAX_REQUESTS_PER_MINUTE=30  # Límite más estricto
```

### 2. Headers de seguridad recomendados
```python
# En producción, agregar headers de seguridad
app.add_middleware(
    SecurityHeadersMiddleware,
    force_https=True,
    strict_transport_security=True,
    content_type_nosniff=True,
    xss_protection=True
)
```

### 3. Logging de seguridad
```python
# Configurar logging de seguridad
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('security.log'),
        logging.StreamHandler()
    ]
)
```

## Próximos pasos

Una vez completado este paso:
1. Verifica que la autenticación funciona correctamente
2. Prueba los diferentes roles y permisos
3. Escribe `continuar` para proceder al **PASO 7** (Dockerizar y preparar migración)

## Notas importantes

- ⚠️ Los tokens se almacenan en memoria (no persistir entre reinicios)
- ✅ Rate limiting por IP para prevenir abuso
- ✅ Logging completo de eventos de seguridad
- ✅ Tokens de desarrollo para testing fácil
- ✅ Sistema de permisos granular por rol
- ✅ Configuración flexible para desarrollo/producción

## Recomendaciones de seguridad

1. **Usar HTTPS en producción**
2. **Rotar SECRET_KEY regularmente**
3. **Monitorear logs de seguridad**
4. **Implementar base de datos para tokens en producción**
5. **Configurar firewall y proxy reverso**
6. **Auditar permisos regularmente**
