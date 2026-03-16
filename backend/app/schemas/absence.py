"""
Schemas Pydantic para el módulo de ausencias.
"""
from pydantic import BaseModel, Field, model_validator
from datetime import datetime
from datetime import date as date_type
from typing import Optional
from app.schemas.employee import EmployeeResponse

VALID_ABSENCE_TYPES = ["vacaciones", "baja_medica", "asunto_personal", "otro"]


class AbsenceBase(BaseModel):
    """Campos comunes para ausencias."""
    employee_id:  int      = Field(..., description="ID del empleado")
    absence_type: str      = Field("vacaciones", description="Tipo de ausencia")
    start_date:   date_type = Field(..., description="Fecha de inicio")
    end_date:     date_type = Field(..., description="Fecha de fin")
    reason:       Optional[str] = Field(None, description="Motivo de la ausencia")

    @model_validator(mode="after")
    def validate_dates(self):
        """Valida que la fecha de fin no sea anterior a la de inicio."""
        if self.end_date < self.start_date:
            raise ValueError("La fecha de fin no puede ser anterior a la de inicio")
        return self


class AbsenceCreate(AbsenceBase):
    """Schema para crear una ausencia."""
    pass


class AbsenceUpdate(BaseModel):
    """Schema para actualizar una ausencia. Todos los campos opcionales."""
    absence_type: Optional[str]      = None
    start_date:   Optional[date_type] = None
    end_date:     Optional[date_type] = None
    reason:       Optional[str]      = None
    is_approved:  Optional[bool]     = None


class AbsenceResponse(AbsenceBase):
    """Schema de respuesta simple."""
    id:          int
    is_approved: bool
    is_active:   bool
    created_at:  datetime
    updated_at:  datetime

    model_config = {"from_attributes": True}


class AbsenceDetailResponse(AbsenceBase):
    """Schema de respuesta enriquecida con datos del empleado."""
    id:          int
    is_approved: bool
    is_active:   bool
    created_at:  datetime
    updated_at:  datetime
    employee:    EmployeeResponse

    model_config = {"from_attributes": True}