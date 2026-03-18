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

geolocator = Nominatim(user_agent="garden_manager_mlg_v3", timeout=15)


def geocode_all_clients():
    db = SessionLocal()
    COORDS_ZONA = {
        "churriana":    (36.6697, -4.5539),
        "guadalmar":    (36.6748, -4.5367),
        "torremolinos": (36.6213, -4.4993),
        "málaga":       (36.7213, -4.4214),
        "malaga":       (36.7213, -4.4214),
        "cádiz":        (36.6900, -4.5100),
        "cadiz":        (36.6900, -4.5100),
    }
    try:
        clientes = db.query(Client).filter(
            Client.is_active.is_(True),
            Client.latitude.is_(None)
        ).all()

        print(f"🌍 Geocodificando {len(clientes)} clientes sin coordenadas...")
        print(f"⏱️  Tiempo estimado: {len(clientes) * 2:.0f} segundos\n")

        ok    = 0
        fallo = 0

        for i, c in enumerate(clientes):
            try:
                # Intento 1 — dirección completa con código postal
                address_query = f"{c.address}, {c.postal_code}, España" if c.postal_code else f"{c.address}, España"
                location = geolocator.geocode(address_query)
                time.sleep(2)

                # Intento 2 — solo zona y código postal
                if not location and c.postal_code:
                    partes   = c.address.split(",")
                    zona     = ", ".join(partes[-2:]).strip()
                    location = geolocator.geocode(f"{zona}, {c.postal_code}, España")
                    time.sleep(2)

                # Fallback — coordenadas del centro de Málaga con offset
                if not location:
                    address_lower = (c.address or "").lower()
                    coords = next(
                        (v for k, v in COORDS_ZONA.items() if k in address_lower),
                        (36.7213, -4.4214)  # Centro Málaga si no hay zona
                    )
                    c.latitude  = coords[0]
                    c.longitude = coords[1]
                    db.commit()
                    print(f"   📍 [{i+1}/{len(clientes)}] {c.name} — zona: {coords}")
                    ok += 1

            except Exception as e:
                print(f"   ❌ [{i+1}/{len(clientes)}] {c.name} — {e}")
                fallo += 1
                time.sleep(2)

        print(f"\n✅ {ok} geocodificados · ❌ {fallo} fallidos")

    finally:
        db.close()

if __name__ == "__main__":
    geocode_all_clients()