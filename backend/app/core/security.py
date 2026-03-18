"""
Utilidades de seguridad: JWT tokens y hashing de contraseñas.
"""
from datetime import datetime, timedelta
from typing import Optional
import secrets
import string

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

# Contexto de hashing — bcrypt es el estándar actual
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hashea una contraseña con bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica que una contraseña coincide con su hash."""
    return pwd_context.verify(plain_password, hashed_password)


def generate_secure_password(length: int = 12) -> str:
    """
    Genera una contraseña segura aleatoria.
    Incluye mayúsculas, minúsculas, números y símbolos.
    """
    alphabet = string.ascii_letters + string.digits + "!@#$%&*"
    while True:
        password = "".join(secrets.choice(alphabet) for _ in range(length))
        # Verifica que tenga al menos uno de cada tipo
        if (
            any(c.islower() for c in password)
            and any(c.isupper() for c in password)
            and any(c.isdigit() for c in password)
            and any(c in "!@#$%&*" for c in password)
        ):
            return password


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Crea un JWT token de acceso.

    Args:
        data: Datos a incluir en el token (normalmente {"sub": email})
        expires_delta: Tiempo de expiración (por defecto 8 horas)

    Returns:
        Token JWT firmado
    """
    to_encode = data.copy()
    expire    = datetime.utcnow() + (expires_delta or timedelta(hours=8))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)


def create_reset_token(email: str) -> str:
    """
    Crea un token de un solo uso para resetear contraseña.
    Expira en 24 horas.
    """
    return create_access_token(
        data={"sub": email, "type": "reset"},
        expires_delta=timedelta(hours=24)
    )


def verify_token(token: str) -> Optional[dict]:
    """
    Verifica y decodifica un JWT token.

    Returns:
        Payload del token si es válido, None si no
    """
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        return payload
    except JWTError:
        return None