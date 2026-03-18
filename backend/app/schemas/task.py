"""
Schemas Pydantic para el módulo de tareas.
"""
from pydantic import BaseModel, Field
from datetime import datetime
from datetime import date as date_type
from datetime import time as time_type
from typing import Optional
from app.schemas.client import ClientResponse
from app.schemas.employee import EmployeeResponse


# Valores permitidos para status y priority
VALID_STATUSES  = ["pendiente", "en_progreso", "completada", "cancelada"]
VALID_PRIORITIES = ["baja", "media", "alta"]


class TaskBase(BaseModel):
    """Campos comunes compartidos entre schemas."""
    title:       str                = Field(..., min_length=2, max_length=150, description="Título de la tarea")
    description: Optional[str]      = Field(None, description="Descripción detallada")
    date:        date_type          = Field(..., description="Fecha programada")
    start_time:  Optional[time_type]= Field(None, description="Hora de inicio")
    end_time:    Optional[time_type]= Field(None, description="Hora de finalización")
    status:      str                = Field("pendiente", description="Estado de la tarea")
    priority:    str                = Field("media",     description="Prioridad")
    client_id:   int                = Field(..., description="ID del cliente")
    notes:       Optional[str]      = Field(None, description="Observaciones")


class TaskCreate(TaskBase):
    """Schema para crear una tarea. Incluye los IDs de empleados a asignar."""
    employee_ids: list[int] = Field(default=[], description="IDs de empleados asignados")


class TaskUpdate(BaseModel):
    """Schema para actualizar una tarea. Todos los campos son opcionales."""
    title:        Optional[str]       = Field(None, min_length=2, max_length=150)
    description:  Optional[str]       = None
    date:         Optional[date_type]      = None
    start_time:   Optional[time_type]      = None
    end_time:     Optional[time_type]      = None
    status:       Optional[str]       = None
    priority:     Optional[str]       = None
    notes:        Optional[str]       = None
    employee_ids: Optional[list[int]] = None


class TaskResponse(TaskBase):
    """Schema de respuesta completa con objetos relacionados."""
    id:         int
    is_active:  bool
    created_at: datetime
    updated_at: datetime
    client:     Optional[ClientResponse]   = None
    employees:  list[EmployeeResponse]     = []
    model_config = {"from_attributes": True}


class TaskDetailResponse(TaskBase):
    """
    Schema de respuesta enriquecida.
    Devuelve objetos completos de cliente y empleados.
    Se usa en el endpoint de detalle de una tarea.
    """
    id:         int
    is_active:  bool
    created_at: datetime
    updated_at: datetime
    client:     ClientResponse
    employees:  list[EmployeeResponse] = []

    model_config = {"from_attributes": True}