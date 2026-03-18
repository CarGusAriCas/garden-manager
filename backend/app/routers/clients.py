"""
Router de clientes.
Define los endpoints HTTP del módulo de clientes.
Solo recibe peticiones y delega al servicio — sin lógica de negocio aquí.
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.client import ClientCreate, ClientUpdate, ClientResponse
import app.services.client_service as client_service

router = APIRouter(
    prefix="/clients",
    tags=["Clientes"]
)


@router.get("/", response_model=list[ClientResponse])
def list_clients(
    skip:  int = Query(default=0,   ge=0,  description="Registros a saltar"),
    limit: int = Query(default=100, ge=1, le=500, description="Límite de resultados"),
    db: Session = Depends(get_db)
):
    """Devuelve la lista de todos los clientes activos."""
    return client_service.get_all_clients(db, skip=skip, limit=limit)


@router.get("/{client_id}", response_model=ClientResponse)
def get_client(client_id: int, db: Session = Depends(get_db)):
    """Devuelve un cliente específico por su ID."""
    return client_service.get_client_by_id(db, client_id)


@router.post("/", response_model=ClientResponse, status_code=201)
def create_client(client_data: ClientCreate, db: Session = Depends(get_db)):
    """Crea un nuevo cliente."""
    return client_service.create_client(db, client_data)


@router.put("/{client_id}", response_model=ClientResponse)
def update_client(client_id: int, client_data: ClientUpdate, db: Session = Depends(get_db)):
    """Actualiza los datos de un cliente existente."""
    return client_service.update_client(db, client_id, client_data)


@router.delete("/{client_id}")
def delete_client(client_id: int, db: Session = Depends(get_db)):
    """Desactiva un cliente (borrado lógico)."""
    return client_service.delete_client(db, client_id)


@router.patch("/{client_id}/coordinates")
def set_client_coordinates(
    client_id: int,
    lat: float,
    lon: float,
    db: Session = Depends(get_db)
):
    """Actualiza las coordenadas geográficas de un cliente."""
    return client_service.update_client_coordinates(db, client_id, lat, lon)


@router.post("/geocode-all")
def geocode_all_clients(db: Session = Depends(get_db)):
    """
    Geocodifica todos los clientes sin coordenadas.
    Ejecutar una sola vez tras el seed inicial.
    """
    import time
    from geopy.geocoders import Nominatim

    geolocator = Nominatim(user_agent="garden_manager_prod_v1", timeout=15)
    clientes    = db.query(Client).filter(
        Client.is_active.is_(True),
        Client.latitude.is_(None)
    ).all()

    resultados = {"ok": 0, "fallo": 0, "total": len(clientes)}

    for c in clientes:
        try:
            query    = f"{c.address}, {c.postal_code}, España" if c.postal_code else f"{c.address}, España"
            location = geolocator.geocode(query)
            time.sleep(1.5)

            if not location:
                partes   = c.address.split(",")
                zona     = ", ".join(partes[-2:]).strip()
                location = geolocator.geocode(f"{zona}, España")
                time.sleep(1.5)

            if location:
                c.latitude  = location.latitude
                c.longitude = location.longitude
                db.commit()
                resultados["ok"] += 1
            else:
                c.latitude  = 36.7213 + (resultados["fallo"] * 0.001)
                c.longitude = -4.4214 + (resultados["fallo"] * 0.001)
                db.commit()
                resultados["fallo"] += 1

        except Exception:
            resultados["fallo"] += 1
            time.sleep(2)

    return resultados