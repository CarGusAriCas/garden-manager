"""
Script para geocodificar todos los clientes de una vez.
Ejecutar manualmente: python geocode_clients.py
Respeta el límite de Nominatim: 1 petición/segundo.
"""
import time
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

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
        print(f"⏱️  Tiempo estimado: {len(clientes) * 1.5:.0f} segundos\n")

        ok = 0
        fallo = 0

        for i, c in enumerate(clientes):
            try:
                location = geolocator.geocode(c.address)
                if location:
                    c.latitude  = location.latitude
                    c.longitude = location.longitude
                    db.commit()
                    print(f"   ✅ [{i+1}/{len(clientes)}] {c.name}")
                    ok += 1
                else:
                    print(f"   ⚠️  [{i+1}/{len(clientes)}] {c.name} — dirección no encontrada")
                    fallo += 1
            except (GeocoderTimedOut, GeocoderUnavailable) as e:
                print(f"   ❌ [{i+1}/{len(clientes)}] {c.name} — {e}")
                fallo += 1

            # Respeta el límite de Nominatim: máximo 1 req/segundo
            time.sleep(1.5)

        print(f"\n✅ {ok} geocodificados · ❌ {fallo} fallidos")

    finally:
        db.close()

if __name__ == "__main__":
    geocode_all_clients()