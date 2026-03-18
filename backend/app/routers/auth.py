"""
Router de autenticación.
Endpoints para login, activación y gestión de usuarios.
"""
from fastapi import APIRouter, Depends, Header
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Optional

from app.core.database import get_db
from app.schemas.user import (
    UserCreate, UserResponse, TokenResponse,
    ChangePasswordRequest, ResetPasswordRequest
)
from app.services import auth_service

router = APIRouter(
    prefix="/auth",
    tags=["Autenticación"]
)


@router.post("/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Login con email y contraseña.
    Devuelve un JWT token válido por 8 horas.
    """
    return auth_service.login(db, form_data.username, form_data.password)


@router.post("/users", status_code=201)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Crea un nuevo usuario y envía email de activación.
    Solo accesible por admin y encargado.
    """
    resultado = auth_service.create_user(db, user_data)
    return {
        "message":       resultado["message"],
        "temp_password": resultado["temp_password"],
        "user": {
            "id":    resultado["user"].id,
            "email": resultado["user"].email,
            "role":  resultado["user"].role,
        }
    }


@router.post("/activate")
def activate_account(data: ChangePasswordRequest, db: Session = Depends(get_db)):
    """Activa una cuenta nueva y establece la contraseña definitiva."""
    return auth_service.activate_account(
        db, data.token, data.new_password, data.confirm_password
    )


@router.post("/reset-password/request")
def request_reset(data: ResetPasswordRequest, db: Session = Depends(get_db)):
    """Solicita el reset de contraseña. Envía email con link."""
    return auth_service.request_password_reset(db, data.email)


@router.post("/reset-password/confirm")
def confirm_reset(data: ChangePasswordRequest, db: Session = Depends(get_db)):
    """Confirma el reset de contraseña con el token del email."""
    return auth_service.reset_password(
        db, data.token, data.new_password, data.confirm_password
    )


@router.get("/me", response_model=UserResponse)
def get_me(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """Devuelve los datos del usuario autenticado."""
    token = authorization.replace("Bearer ", "") if authorization else ""
    user  = auth_service.get_current_user(db, token)
    return user


@router.get("/users", response_model=list[UserResponse])
def list_users(db: Session = Depends(get_db)):
    """Lista todos los usuarios. Solo para admin."""
    from app.models.user import User
    return db.query(User).all()