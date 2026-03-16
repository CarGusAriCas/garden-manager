"""
Schemas Pydantic para el módulo de clientes.
Definen qué datos se aceptan y qué datos se devuelven en cada operación.
"""
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


class ClientBase(BaseModel):
    """Campos comunes compartidos entre schemas."""
    name:    str            = Field(..., min_length=2, max_length=100, description="Nombre completo")
    phone:   Optional[str] = Field(None, max_length=20, description="Teléfono de contacto")
    email:   Optional[EmailStr] = Field(None, description="Correo electrónico")
    address: Optional[str] = Field(None, max_length=200, description="Dirección del inmueble")
    notes:   Optional[str] = Field(None, max_length=500, description="Observaciones")


class ClientCreate(ClientBase):
    """Schema para crear un cliente. Hereda todos los campos de ClientBase."""
    pass


class ClientUpdate(BaseModel):
    """
    Schema para actualizar un cliente.
    Todos los campos son opcionales — solo se actualizan los que se envían.
    """
    name:      Optional[str]      = Field(None, min_length=2, max_length=100)
    phone:     Optional[str]      = Field(None, max_length=20)
    email:     Optional[EmailStr] = None
    address:   Optional[str]      = Field(None, max_length=200)
    notes:     Optional[str]      = Field(None, max_length=500)
    is_active: Optional[bool]     = None


class ClientResponse(ClientBase):
    """
    Schema de respuesta. Incluye campos generados por la BD.
    Este es el formato que devuelve la API al cliente.
    """
    id:         int
    is_active:  bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}