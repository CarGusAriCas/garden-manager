"""
Modelo de base de datos para las tareas.
Define la tabla 'tasks' y la tabla de asociación 'task_employees'.
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, Time, ForeignKey, Table, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


# Tabla de asociación many-to-many entre tareas y empleados
# No tiene modelo propio — solo conecta IDs
task_employees = Table(
    "task_employees",
    Base.metadata,
    Column("task_id",     Integer, ForeignKey("tasks.id"),     primary_key=True),
    Column("employee_id", Integer, ForeignKey("employees.id"), primary_key=True),
)


class Task(Base):
    """
    Tabla 'tasks' en la base de datos.

    Atributos:
        id: Identificador único autoincremental
        title: Título descriptivo de la tarea
        description: Descripción detallada del trabajo a realizar
        date: Fecha programada
        start_time: Hora de inicio
        end_time: Hora de finalización estimada
        status: Estado actual (pendiente, en_progreso, completada, cancelada)
        priority: Prioridad (baja, media, alta)
        client_id: Cliente al que pertenece la tarea
        notes: Observaciones adicionales
        is_active: Para borrado lógico
        created_at: Fecha de creación automática
        updated_at: Fecha de última modificación automática
        client: Relación con el objeto Client
        employees: Relación many-to-many con Employee
    """
    __tablename__ = "tasks"

    id          = Column(Integer,      primary_key=True, index=True)
    title       = Column(String(150),  nullable=False)
    description = Column(Text,         nullable=True)
    date        = Column(Date,         nullable=False, index=True)
    start_time  = Column(Time,         nullable=True)
    end_time    = Column(Time,         nullable=True)
    status      = Column(String(20),   nullable=False, default="pendiente", index=True)
    priority    = Column(String(10),   nullable=False, default="media", index=True)
    client_id   = Column(Integer,      ForeignKey("clients.id"), nullable=False, index=True)
    notes       = Column(Text,         nullable=True)
    is_active   = Column(Boolean,      default=True, index=True)
    created_at  = Column(DateTime,     server_default=func.now())
    updated_at  = Column(DateTime,     server_default=func.now(), onupdate=func.now())

    # Relaciones
    client    = relationship("Client",   back_populates="tasks")
    employees = relationship("Employee", secondary=task_employees, back_populates="tasks")
    # Relación: una tarea puede tener un trabajo asociado
    jobs = relationship("Job", back_populates="task")