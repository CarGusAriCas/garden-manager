"""
Servicio de autenticación.
Gestiona usuarios, login, activación y reset de contraseña.
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user import User
from app.models.employee import Employee
from app.schemas.user import UserCreate
from app.core.security import (
    hash_password, verify_password,
    generate_secure_password,
    create_access_token, create_reset_token,
    verify_token
)
from app.core.email import send_activation_email, send_password_reset_email


def get_user_by_email(db: Session, email: str) -> User:
    """Obtiene un usuario por email."""
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user_data: UserCreate) -> dict:
    """
    Crea un nuevo usuario y envía email de activación.

    Args:
        db: Sesión de base de datos
        user_data: Datos del nuevo usuario

    Returns:
        Diccionario con el usuario creado y la contraseña temporal

    Raises:
        HTTPException 400: Si el email ya existe
        HTTPException 404: Si el employee_id no existe
    """
    # Verifica email único
    if get_user_by_email(db, user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El email {user_data.email} ya está registrado"
        )

    # Verifica que el empleado existe si se vincula
    empleado = None
    if user_data.employee_id:
        empleado = db.query(Employee).filter(Employee.id == user_data.employee_id).first()
        if not empleado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Empleado con ID {user_data.employee_id} no encontrado"
            )

    # Genera contraseña segura temporal
    temp_password = generate_secure_password()

    # Crea el usuario
    db_user = User(
        email           = user_data.email,
        hashed_password = hash_password(temp_password),
        role            = user_data.role,
        employee_id     = user_data.employee_id,
        is_active       = False,
        must_change_password = True,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # Genera token de activación
    token  = create_reset_token(user_data.email)
    nombre = empleado.name if empleado else user_data.email

    # Envía email de activación
    send_activation_email(user_data.email, nombre, token)

    return {
        "user":           db_user,
        "temp_password":  temp_password,
        "message":        f"Usuario creado. Email de activación enviado a {user_data.email}"
    }


def login(db: Session, email: str, password: str) -> dict:
    """
    Autentica un usuario y devuelve un JWT token.

    Args:
        db: Sesión de base de datos
        email: Email del usuario
        password: Contraseña en texto plano

    Returns:
        Diccionario con token, rol y nombre

    Raises:
        HTTPException 401: Si las credenciales son incorrectas
        HTTPException 403: Si la cuenta no está activada
    """
    user = get_user_by_email(db, email)

    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cuenta no activada. Revisa tu email."
        )

    # Obtiene el nombre del empleado vinculado
    nombre = user.email
    if user.employee_id:
        empleado = db.query(Employee).filter(Employee.id == user.employee_id).first()
        if empleado:
            nombre = empleado.name

    token = create_access_token(data={"sub": user.email, "role": user.role})

    return {
        "access_token":          token,
        "token_type":            "bearer",
        "role":                  user.role,
        "nombre":                nombre,
        "employee_id":           user.employee_id,
        "must_change_password":  user.must_change_password,
    }


def activate_account(db: Session, token: str, new_password: str, confirm_password: str) -> dict:
    """
    Activa una cuenta y establece la contraseña definitiva.
    """
    if new_password != confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Las contraseñas no coinciden"
        )

    payload = verify_token(token)
    if not payload or payload.get("type") != "reset":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token inválido o expirado"
        )

    user = get_user_by_email(db, payload["sub"])
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    # Actualiza campos explícitamente
    db.query(User).filter(User.id == user.id).update({
        "hashed_password":      hash_password(new_password),
        "is_active":            True,
        "must_change_password": False,
    })
    db.commit()

    return {"message": "Cuenta activada correctamente. Ya puedes iniciar sesión."}


def request_password_reset(db: Session, email: str) -> dict:
    """
    Envía email de reset de contraseña.
    No revela si el email existe o no por seguridad.
    """
    user = get_user_by_email(db, email)
    if user:
        token  = create_reset_token(email)
        nombre = email
        if user.employee_id:
            emp = db.query(Employee).filter(Employee.id == user.employee_id).first()
            if emp:
                nombre = emp.name
        send_password_reset_email(email, nombre, token)

    return {"message": "Si el email existe recibirás instrucciones para restablecer tu contraseña."}


def reset_password(db: Session, token: str, new_password: str, confirm_password: str) -> dict:
    """Restablece la contraseña usando el token de reset."""
    return activate_account(db, token, new_password, confirm_password)


def get_current_user(db: Session, token: str) -> User:
    """
    Obtiene el usuario actual a partir del JWT token.
    Se usa como dependencia en los endpoints protegidos.

    Raises:
        HTTPException 401: Si el token es inválido
    """
    payload = verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = get_user_by_email(db, payload["sub"])
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado o inactivo"
        )
    return user