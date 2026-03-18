"""
Schemas Pydantic para el módulo de usuarios y autenticación.
"""
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

VALID_ROLES = ["admin", "encargado", "empleado"]


class UserCreate(BaseModel):
    """Schema para crear un usuario. Lo usa el admin."""
    email:       EmailStr = Field(..., description="Email de login")
    role:        str      = Field("empleado", description="Rol del usuario")
    employee_id: Optional[int] = Field(None, description="ID del empleado vinculado")


class UserResponse(BaseModel):
    """Schema de respuesta de usuario."""
    id:                   int
    email:                str
    role:                 str
    employee_id:          Optional[int]
    is_active:            bool
    must_change_password: bool
    created_at:           datetime

    model_config = {"from_attributes": True}


class LoginRequest(BaseModel):
    """Schema para el login."""
    email:    EmailStr = Field(..., description="Email de login")
    password: str      = Field(..., description="Contraseña")


class TokenResponse(BaseModel):
    """Respuesta del endpoint de login."""
    access_token:         str
    token_type:           str = "bearer"
    role:                 str
    nombre:               str
    employee_id:          Optional[int] = None
    must_change_password: bool


class ChangePasswordRequest(BaseModel):
    """Schema para cambiar contraseña."""
    token:        str = Field(..., description="Token de activación o reset")
    new_password: str = Field(..., min_length=8, description="Nueva contraseña")
    confirm_password: str = Field(..., description="Confirmación de contraseña")


class ResetPasswordRequest(BaseModel):
    """Schema para solicitar reset de contraseña."""
    email: EmailStr