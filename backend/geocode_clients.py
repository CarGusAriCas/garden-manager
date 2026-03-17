"""
Script para geocodificar todos los clientes de una vez.
Ejecutar manualmente: python geocode_clients.py
"""
import time
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Importa todos los modelos para que SQLAlchemy resuelva las relaciones
from app.models import client, employee, task, job, absence
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
                # Intento 1 — dirección completa
                location = geolocator.geocode(c.address)

                # Intento 2 — solo la zona (última parte de la dirección)
                if not location:
                    partes   = c.address.split(",")
                    zona     = ", ".join(partes[-2:]).strip() if len(partes) > 1 else c.address
                    location = geolocator.geocode(zona)
                    time.sleep(1.5)

                # Intento 3 — solo ciudad
                if not location:
                    ciudad   = partes[-1].strip() if partes else "Málaga"
                    location = geolocator.geocode(f"{ciudad}, España")
                    time.sleep(1.5)

                if location:
                    c.latitude  = location.latitude
                    c.longitude = location.longitude
                    db.commit()
                    print(f"   ✅ [{i+1}/{len(clientes)}] {c.name} → {location.address[:50]}")
                    ok += 1
                else:
                    # Fallback — coordenadas del centro de Málaga
                    c.latitude  = 36.7213 + (i * 0.001)  # pequeño offset para no apilar
                    c.longitude = -4.4214 + (i * 0.001)
                    db.commit()
                    print(f"   📍 [{i+1}/{len(clientes)}] {c.name} — usando centro Málaga")
                    ok += 1

            except (GeocoderTimedOut, GeocoderUnavailable) as e:
                print(f"   ❌ [{i+1}/{len(clientes)}] {c.name} — {e}")
                fallo += 1

            time.sleep(1.5)

        print(f"\n✅ {ok} geocodificados · ❌ {fallo} fallidos")

    finally:
        db.close()

if __name__ == "__main__":
    geocode_all_clients()