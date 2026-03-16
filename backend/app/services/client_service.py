"""
Servicio de clientes.
Contiene toda la lógica de negocio del módulo de clientes.
Los routers llaman a estas funciones — nunca acceden a la BD directamente.
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.client import Client
from app.schemas.client import ClientCreate, ClientUpdate


def get_all_clients(db: Session, skip: int = 0, limit: int = 100) -> list[Client]:
    """
    Obtiene todos los clientes activos con paginación.

    Args:
        db: Sesión de base de datos
        skip: Número de registros a saltar (para paginación)
        limit: Número máximo de registros a devolver

    Returns:
        Lista de clientes activos
    """
    return db.query(Client).filter(Client.is_active == True).offset(skip).limit(limit).all()


def get_client_by_id(db: Session, client_id: int) -> Client:
    """
    Obtiene un cliente por su ID.

    Args:
        db: Sesión de base de datos
        client_id: ID del cliente a buscar

    Returns:
        Cliente encontrado

    Raises:
        HTTPException 404: Si el cliente no existe
    """
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cliente con ID {client_id} no encontrado"
        )
    return client


def create_client(db: Session, client_data: ClientCreate) -> Client:
    """
    Crea un nuevo cliente en la base de datos.

    Args:
        db: Sesión de base de datos
        client_data: Datos validados del nuevo cliente

    Returns:
        Cliente recién creado

    Raises:
        HTTPException 400: Si el email ya está registrado
    """
    if client_data.email:
        existing = db.query(Client).filter(Client.email == client_data.email).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El email {client_data.email} ya está registrado"
            )

    db_client = Client(**client_data.model_dump())
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client


def update_client(db: Session, client_id: int, client_data: ClientUpdate) -> Client:
    """
    Actualiza los datos de un cliente existente.
    Solo modifica los campos que se envían en la petición.

    Args:
        db: Sesión de base de datos
        client_id: ID del cliente a actualizar
        client_data: Campos a actualizar

    Returns:
        Cliente actualizado
    """
    client = get_client_by_id(db, client_id)

    update_data = client_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(client, field, value)

    db.commit()
    db.refresh(client)
    return client


def delete_client(db: Session, client_id: int) -> dict:
    """
    Desactiva un cliente (borrado lógico).
    No se elimina de la BD — se marca como inactivo para conservar el historial.

    Args:
        db: Sesión de base de datos
        client_id: ID del cliente a desactivar

    Returns:
        Mensaje de confirmación
    """
    client = get_client_by_id(db, client_id)
    client.is_active = False
    db.commit()
    return {"message": f"Cliente {client.name} desactivado correctamente"}

def update_client_coordinates(db: Session, client_id: int, lat: float, lon: float) -> Client:
    """
    Actualiza las coordenadas geográficas de un cliente.

    Args:
        db: Sesión de base de datos
        client_id: ID del cliente
        lat: Latitud
        lon: Longitud

    Returns:
        Cliente actualizado
    """
    client           = get_client_by_id(db, client_id)
    client.latitude  = lat
    client.longitude = lon
    db.commit()
    db.refresh(client)
    return client