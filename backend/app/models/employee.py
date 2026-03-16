"""
Modelo de base de datos para los empleados.
Define la tabla 'employees' y sus columnas.
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class Employee(Base):
    """
    Tabla 'employees' en la base de datos.

    Atributos:
        id: Identificador único autoincremental
        name: Nombre completo del empleado
        phone: Teléfono de contacto
        email: Correo electrónico (único)
        role: Cargo o puesto
        speciality: Especialidad
        hire_date: Fecha de incorporación
        is_active: Si el empleado está activo o dado de baja
        created_at: Fecha de creación automática
        updated_at: Fecha de última modificación automática
        tasks: Relación con las tareas asignadas a este empleado
    """
    __tablename__ = "employees"

    id          = Column(Integer, primary_key=True, index=True)
    name        = Column(String(100), nullable=False)
    phone       = Column(String(20),  nullable=True)
    email       = Column(String(100), unique=True, nullable=True)
    role        = Column(String(50),  nullable=False, default="Jardinero")
    speciality  = Column(String(100), nullable=True)
    hire_date   = Column(Date,        nullable=True)
    is_active   = Column(Boolean,     default=True)
    created_at  = Column(DateTime,    server_default=func.now())
    updated_at  = Column(DateTime,    server_default=func.now(), onupdate=func.now())

    # Relación: un empleado puede tener muchas tareas
    tasks = relationship("Task", secondary="task_employees", back_populates="employees")
    # Relación: un empleado puede tener muchas ausencias
    absences = relationship("Absence", back_populates="employee")