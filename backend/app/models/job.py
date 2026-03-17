"""
Modelos de base de datos para trabajos y checklists.
Un trabajo es la ejecución real de una tarea planificada.
Cada trabajo puede tener una lista de ítems de verificación.
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class Job(Base):
    """
    Tabla 'jobs' — registro de trabajos realizados.

    Atributos:
        id: Identificador único
        task_id: Tarea origen que se está ejecutando
        started_at: Fecha y hora de inicio real
        finished_at: Fecha y hora de finalización real
        status: Estado (en_progreso, completado, incompleto)
        notes: Observaciones del equipo al terminar
        is_active: Para borrado lógico
        created_at: Fecha de creación automática
        updated_at: Fecha de última modificación
        task: Relación con la tarea origen
        checklist_items: Ítems de verificación del trabajo
    """
    __tablename__ = "jobs"

    id          = Column(Integer,   primary_key=True, index=True)
    task_id     = Column(Integer,   ForeignKey("tasks.id"), nullable=False, index=True)
    started_at  = Column(DateTime,  nullable=True)
    finished_at = Column(DateTime,  nullable=True)
    status      = Column(String(20),nullable=False, default="en_progreso", index=True)
    notes       = Column(Text,      nullable=True)
    is_active   = Column(Boolean,   default=True, index=True)
    created_at  = Column(DateTime,  server_default=func.now())
    updated_at  = Column(DateTime,  server_default=func.now(), onupdate=func.now())

    # Relaciones
    task             = relationship("Task", back_populates="jobs")
    checklist_items  = relationship("ChecklistItem", back_populates="job", cascade="all, delete-orphan")


class ChecklistItem(Base):
    """
    Tabla 'checklist_items' — ítems de verificación de un trabajo.

    Atributos:
        id: Identificador único
        job_id: Trabajo al que pertenece
        description: Descripción del ítem a verificar
        is_done: Si el ítem se completó correctamente
        has_incident: Si el ítem generó una incidencia
        incident_notes: Descripción del problema encontrado
        created_at: Fecha de creación automática
        job: Relación con el trabajo
    """
    __tablename__ = "checklist_items"

    id             = Column(Integer,    primary_key=True, index=True)
    job_id         = Column(Integer,    ForeignKey("jobs.id"), nullable=False)
    description    = Column(String(200),nullable=False)
    is_done        = Column(Boolean,    default=False)
    has_incident   = Column(Boolean,    default=False)
    incident_notes = Column(Text,       nullable=True)
    created_at     = Column(DateTime,   server_default=func.now())

    # Relación
    job = relationship("Job", back_populates="checklist_items")