#!/usr/bin/env python3
"""
Módulo de seguridad para el bot de Facilitadores Judiciales.
Implementa autenticación básica con tokens y middleware de seguridad.
"""

import os
import secrets
import hashlib
import time
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class SecurityManager:
    """
    Gestor de seguridad para autenticación y autorización.
    """
    
    def __init__(self):
        self.secret_key = os.getenv("SECRET_KEY", self._generate_secret_key())
        self.token_expiry_hours = int(os.getenv("TOKEN_EXPIRY_HOURS", "24"))
        self.max_requests_per_minute = int(os.getenv("MAX_REQUESTS_PER_MINUTE", "60"))
        
        # Almacenamiento simple en memoria (en producción usar Redis/DB)
        self.active_tokens: Dict[str, Dict[str, Any]] = {}
        self.request_counts: Dict[str, List[float]] = {}
        
        # Tokens predefinidos para desarrollo
        self.dev_tokens = {
            "admin": "dev-admin-token-12345",
            "user": "dev-user-token-67890",
            "facilitador": "dev-facilitador-token-abcde"
        }
        
        logger.info("🔐 SecurityManager inicializado")
    
    def _generate_secret_key(self) -> str:
        """
        Genera una clave secreta aleatoria.
        """
        return secrets.token_urlsafe(32)
    
    def generate_token(self, user_id: str, role: str = "user") -> str:
        """
        Genera un token de autenticación para un usuario.
        """
        # Crear payload del token
        payload = {
            "user_id": user_id,
            "role": role,
            "created_at": time.time(),
            "expires_at": time.time() + (self.token_expiry_hours * 3600)
        }
        
        # Generar token único
        token_data = f"{user_id}:{role}:{payload['created_at']}:{self.secret_key}"
        token = hashlib.sha256(token_data.encode()).hexdigest()
        
        # Almacenar token
        self.active_tokens[token] = payload
        
        logger.info(f"Token generado para usuario: {user_id} con rol: {role}")
        return token
    
    def validate_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Valida un token de autenticación.
        """
        if not token:
            return None
        
        # Verificar token en almacenamiento
        if token in self.active_tokens:
            payload = self.active_tokens[token]
            
            # Verificar expiración
            if time.time() > payload["expires_at"]:
                del self.active_tokens[token]
                logger.warning(f"Token expirado: {token[:8]}...")
                return None
            
            return payload
        
        # Verificar tokens de desarrollo
        if token in self.dev_tokens.values():
            for user_id, dev_token in self.dev_tokens.items():
                if dev_token == token:
                    return {
                        "user_id": user_id,
                        "role": "admin" if user_id == "admin" else "user",
                        "created_at": time.time() - 3600,  # Simular token creado hace 1 hora
                        "expires_at": time.time() + (self.token_expiry_hours * 3600)
                    }
        
        logger.warning(f"Token inválido: {token[:8]}...")
        return None
    
    def revoke_token(self, token: str) -> bool:
        """
        Revoca un token de autenticación.
        """
        if token in self.active_tokens:
            del self.active_tokens[token]
            logger.info(f"Token revocado: {token[:8]}...")
            return True
        return False
    
    def check_rate_limit(self, client_ip: str) -> bool:
        """
        Verifica si el cliente ha excedido el límite de requests.
        """
        now = time.time()
        minute_ago = now - 60
        
        # Limpiar requests antiguos
        if client_ip in self.request_counts:
            self.request_counts[client_ip] = [
                req_time for req_time in self.request_counts[client_ip]
                if req_time > minute_ago
            ]
        else:
            self.request_counts[client_ip] = []
        
        # Verificar límite
        if len(self.request_counts[client_ip]) >= self.max_requests_per_minute:
            logger.warning(f"Rate limit excedido para IP: {client_ip}")
            return False
        
        # Agregar request actual
        self.request_counts[client_ip].append(now)
        return True
    
    def get_user_permissions(self, role: str) -> Dict[str, bool]:
        """
        Obtiene los permisos de un rol.
        """
        permissions = {
            "admin": {
                "read": True,
                "write": True,
                "delete": True,
                "manage_users": True,
                "view_logs": True
            },
            "facilitador": {
                "read": True,
                "write": True,
                "delete": False,
                "manage_users": False,
                "view_logs": False
            },
            "user": {
                "read": True,
                "write": False,
                "delete": False,
                "manage_users": False,
                "view_logs": False
            }
        }
        
        return permissions.get(role, permissions["user"])
    
    def cleanup_expired_tokens(self):
        """
        Limpia tokens expirados del almacenamiento.
        """
        now = time.time()
        expired_tokens = [
            token for token, payload in self.active_tokens.items()
            if now > payload["expires_at"]
        ]
        
        for token in expired_tokens:
            del self.active_tokens[token]
        
        if expired_tokens:
            logger.info(f"Limpiados {len(expired_tokens)} tokens expirados")
    
    def get_security_stats(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas de seguridad.
        """
        return {
            "active_tokens": len(self.active_tokens),
            "total_requests_last_hour": sum(
                len(requests) for requests in self.request_counts.values()
            ),
            "unique_ips": len(self.request_counts),
            "token_expiry_hours": self.token_expiry_hours,
            "max_requests_per_minute": self.max_requests_per_minute
        }

# Instancia global del gestor de seguridad
security_manager = SecurityManager()

def get_security_manager() -> SecurityManager:
    """
    Obtiene la instancia del gestor de seguridad.
    """
    return security_manager

def create_dev_tokens() -> Dict[str, str]:
    """
    Crea tokens de desarrollo para testing.
    """
    tokens = {}
    for user_id, role in [("admin", "admin"), ("user", "user"), ("facilitador", "facilitador")]:
        token = security_manager.generate_token(user_id, role)
        tokens[user_id] = token
    
    return tokens

def validate_auth_header(auth_header: str) -> Optional[Dict[str, Any]]:
    """
    Valida el header de autorización.
    """
    if not auth_header:
        return None
    
    # Formato esperado: "Bearer <token>"
    if not auth_header.startswith("Bearer "):
        return None
    
    token = auth_header[7:]  # Remover "Bearer "
    return security_manager.validate_token(token)

def check_permission(user_info: Dict[str, Any], required_permission: str) -> bool:
    """
    Verifica si el usuario tiene el permiso requerido.
    """
    if not user_info:
        return False
    
    role = user_info.get("role", "user")
    permissions = security_manager.get_user_permissions(role)
    
    return permissions.get(required_permission, False)

# Función de utilidad para logging de seguridad
def log_security_event(event_type: str, user_id: str, details: str):
    """
    Registra un evento de seguridad.
    """
    logger.info(f"SECURITY_EVENT: {event_type} | User: {user_id} | Details: {details}")

if __name__ == "__main__":
    # Crear tokens de desarrollo
    print("🔐 Creando tokens de desarrollo...")
    dev_tokens = create_dev_tokens()
    
    print("\nTokens generados:")
    for user_id, token in dev_tokens.items():
        print(f"  {user_id}: {token}")
    
    print(f"\nEstadísticas de seguridad:")
    stats = security_manager.get_security_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
