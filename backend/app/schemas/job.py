"""
Schemas Pydantic para trabajos y checklists.
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


# ── Checklist Items ────────────────────────────────────────────

class ChecklistItemBase(BaseModel):
    """Campos comunes para ítems de checklist."""
    description:    str  = Field(..., min_length=2, max_length=200, description="Descripción del ítem")
    is_done:        bool = Field(False, description="Si el ítem está completado")
    has_incident:   bool = Field(False, description="Si generó una incidencia")
    incident_notes: Optional[str] = Field(None, description="Descripción de la incidencia")


class ChecklistItemCreate(ChecklistItemBase):
    """Schema para crear un ítem de checklist."""
    pass


class ChecklistItemUpdate(BaseModel):
    """Schema para actualizar un ítem. Todos los campos opcionales."""
    description:    Optional[str]  = Field(None, min_length=2, max_length=200)
    is_done:        Optional[bool] = None
    has_incident:   Optional[bool] = None
    incident_notes: Optional[str]  = None


class ChecklistItemResponse(ChecklistItemBase):
    """Schema de respuesta para ítems de checklist."""
    id:         int
    job_id:     int
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Jobs ───────────────────────────────────────────────────────

class JobBase(BaseModel):
    """Campos comunes para trabajos."""
    task_id:     int            = Field(..., description="ID de la tarea origen")
    started_at:  Optional[datetime] = Field(None, description="Inicio real del trabajo")
    finished_at: Optional[datetime] = Field(None, description="Fin real del trabajo")
    status:      str            = Field("en_progreso", description="Estado del trabajo")
    notes:       Optional[str]  = Field(None, description="Observaciones del equipo")


class JobCreate(JobBase):
    """
    Schema para crear un trabajo.
    Permite crear los ítems del checklist al mismo tiempo.
    """
    checklist_items: list[ChecklistItemCreate] = Field(
        default=[], description="Ítems del checklist inicial"
    )


class JobUpdate(BaseModel):
    """Schema para actualizar un trabajo. Todos los campos opcionales."""
    started_at:  Optional[datetime] = None
    finished_at: Optional[datetime] = None
    status:      Optional[str]      = None
    notes:       Optional[str]      = None


class JobResponse(JobBase):
    """Schema de respuesta completa de un trabajo."""
    id:              int
    is_active:       bool
    created_at:      datetime
    updated_at:      datetime
    checklist_items: list[ChecklistItemResponse] = []

    model_config = {"from_attributes": True}