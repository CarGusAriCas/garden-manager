"""
Script para geocodificar todos los clientes de una vez.
Ejecutar manualmente: python geocode_clients.py
"""
import time
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Importa todos los modelos para que SQLAlchemy resuelva las relaciones
from app.models import client, employee, task, job, absence # noqa
from app.core.database import SessionLocal
from app.models.client import Client
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable

geolocator = Nominatim(user_agent="garden_manager_mlg_v2", timeout=10)


def geocode_all_clients():
    db = SessionLocal()
    try:
        clientes = db.query(Client).filter(
            Client.is_active.is_(True),
            Client.latitude.is_(None)
        ).all()

        print(f"🌍 Geocodificando {len(clientes)} clientes sin coordenadas...")

        ok = 0
        fallo = 0

        for i, c in enumerate(clientes):
            try:
                # Construye dirección con código postal si está disponible
                address_query = c.address
                if c.postal_code:
                    address_query = f"{c.address}, {c.postal_code}, España"
                else:
                    address_query = f"{c.address}, España"

                location = geolocator.geocode(address_query)

                # Intento 2 — sin número de calle
                if not location and c.postal_code:
                    partes   = c.address.split(",")
                    zona     = ", ".join(partes[-2:]).strip()
                    location = geolocator.geocode(f"{zona}, {c.postal_code}, España")
                    time.sleep(1.5)

                # Fallback — solo código postal
                if not location and c.postal_code:
                    location = geolocator.geocode(f"{c.postal_code}, España")
                    time.sleep(1.5)
            except (GeocoderTimedOut, GeocoderUnavailable) as e:
                print(f"   ❌ [{i+1}/{len(clientes)}] {c.name} — {e}")
                fallo += 1

            time.sleep(1.5)

        print(f"\n✅ {ok} geocodificados · ❌ {fallo} fallidos")

    finally:
        db.close()

if __name__ == "__main__":
    geocode_all_clients()