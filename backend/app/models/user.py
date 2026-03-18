"""
Modelo de base de datos para usuarios del sistema.
Vinculado opcionalmente con un empleado.
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class User(Base):
    """
    Tabla 'users' en la base de datos.

    Atributos:
        id: Identificador único
        email: Email de login (único)
        hashed_password: Contraseña hasheada con bcrypt
        role: Rol del usuario (admin, encargado, empleado)
        employee_id: FK opcional al empleado vinculado
        is_active: Si el usuario está activo
        must_change_password: True en el primer login
        created_at: Fecha de creación
        updated_at: Fecha de última modificación
        employee: Relación con el empleado vinculado
    """
    __tablename__ = "users"

    id                   = Column(Integer,     primary_key=True, index=True)
    email                = Column(String(100), unique=True, nullable=False, index=True)
    hashed_password      = Column(String(255), nullable=False)
    role                 = Column(String(20),  nullable=False, default="empleado")
    employee_id          = Column(Integer,     ForeignKey("employees.id"), nullable=True)
    is_active            = Column(Boolean,     default=False)  # False hasta activar
    must_change_password = Column(Boolean,     default=True)
    created_at           = Column(DateTime,    server_default=func.now())
    updated_at           = Column(DateTime,    server_default=func.now(), onupdate=func.now())

    # Relación con empleado
    employee = relationship("Employee", back_populates="user")