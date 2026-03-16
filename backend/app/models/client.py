"""
Modelo de base de datos para los clientes.
Define la tabla 'clients' y sus columnas.
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.core.database import Base


class Client(Base):
    """
    Tabla 'clients' en la base de datos.

    Atributos:
        id: Identificador único autoincremental
        name: Nombre completo del cliente
        phone: Teléfono de contacto
        email: Correo electrónico (único)
        address: Dirección del inmueble a tratar
        notes: Observaciones adicionales
        is_active: Si el cliente está activo o dado de baja
        created_at: Fecha de creación automática
        updated_at: Fecha de última modificación automática
    """
    __tablename__ = "clients"

    id         = Column(Integer, primary_key=True, index=True)
    name       = Column(String(100), nullable=False)
    phone      = Column(String(20), nullable=True)
    email      = Column(String(100), unique=True, nullable=True)
    address    = Column(String(200), nullable=True)
    notes      = Column(String(500), nullable=True)
    is_active  = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())