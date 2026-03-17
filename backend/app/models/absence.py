"""
Modelo de base de datos para las ausencias de personal.
Registra vacaciones, bajas médicas y otros tipos de ausencia.
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class Absence(Base):
    """
    Tabla 'absences' en la base de datos.

    Atributos:
        id: Identificador único
        employee_id: Empleado al que pertenece la ausencia
        absence_type: Tipo de ausencia (vacaciones, baja_medica, asunto_personal, otro)
        start_date: Fecha de inicio de la ausencia
        end_date: Fecha de fin de la ausencia
        reason: Motivo o descripción adicional
        is_approved: Si la ausencia está aprobada por el encargado
        is_active: Para borrado lógico
        created_at: Fecha de creación automática
        updated_at: Fecha de última modificación
        employee: Relación con el empleado
    """
    __tablename__ = "absences"

    id           = Column(Integer,    primary_key=True, index=True)
    employee_id  = Column(Integer,    ForeignKey("employees.id"), nullable=False, index=True)
    absence_type = Column(String(30), nullable=False, default="vacaciones")
    start_date   = Column(Date,       nullable=False, index=True)
    end_date     = Column(Date,       nullable=False, index=True)
    reason       = Column(Text,       nullable=True)
    is_approved  = Column(Boolean,    default=False, index=True)
    is_active    = Column(Boolean,    default=True, index=True)
    created_at   = Column(DateTime,   server_default=func.now())
    updated_at   = Column(DateTime,   server_default=func.now(), onupdate=func.now())

    # Relación
    employee = relationship("Employee", back_populates="absences")