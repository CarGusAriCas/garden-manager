"""
Schemas Pydantic para el módulo de empleados.
Definen qué datos se aceptan y qué datos se devuelven en cada operación.
"""
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, date
from typing import Optional


class EmployeeBase(BaseModel):
    """Campos comunes compartidos entre schemas."""
    name:       str            = Field(..., min_length=2, max_length=100, description="Nombre completo")
    phone:      Optional[str]  = Field(None, max_length=20,  description="Teléfono de contacto")
    email:      Optional[EmailStr] = Field(None,             description="Correo electrónico")
    role:       str            = Field("Jardinero", max_length=50,  description="Cargo o puesto")
    speciality: Optional[str]  = Field(None, max_length=100, description="Especialidad")
    hire_date:  Optional[date] = Field(None,                 description="Fecha de incorporación")
    latitude:  Optional[float] = Field(None, description="Latitud")
    longitude: Optional[float] = Field(None, description="Longitud")


class EmployeeCreate(EmployeeBase):
    """Schema para crear un empleado. Hereda todos los campos de EmployeeBase."""
    pass


class EmployeeUpdate(BaseModel):
    """
    Schema para actualizar un empleado.
    Todos los campos son opcionales — solo se actualizan los que se envían.
    """
    name:       Optional[str]      = Field(None, min_length=2, max_length=100)
    phone:      Optional[str]      = Field(None, max_length=20)
    email:      Optional[EmailStr] = None
    role:       Optional[str]      = Field(None, max_length=50)
    speciality: Optional[str]      = Field(None, max_length=100)
    hire_date:  Optional[date]     = None
    is_active:  Optional[bool]     = None


class EmployeeResponse(EmployeeBase):
    """
    Schema de respuesta. Incluye campos generados por la BD.
    Este es el formato que devuelve la API al cliente.
    """
    id:         int
    is_active:  bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}