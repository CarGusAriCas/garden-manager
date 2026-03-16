"""
Script para poblar la base de datos con datos de prueba.
Ejecutar una sola vez: python seed.py
"""
import requests

BASE_URL = "http://localhost:8000"

# ── Clientes ───────────────────────────────────────────────────
clientes = [
    {
        "name": "María García",
        "phone": "612345678",
        "email": "maria@ejemplo.com",
        "address": "Calle Mayor 12, Madrid",
        "notes": "Jardín de 200m². Cliente desde 2023."
    },
    {
        "name": "Juan Martínez",
        "phone": "623456789",
        "email": "juan@ejemplo.com",
        "address": "Avenida del Parque 5, Madrid",
        "notes": "Terraza y jardín trasero."
    },
    {
        "name": "Empresa Logística S.L.",
        "phone": "914567890",
        "email": "contacto@logistica.com",
        "address": "Polígono Industrial Norte, Nave 3",
        "notes": "Mantenimiento de zonas verdes de la nave."
    },
]

# ── Empleados ──────────────────────────────────────────────────
empleados = [
    {
        "name": "Carlos Ruiz",
        "phone": "634567890",
        "email": "carlos@jardineria.com",
        "role": "Encargado",
        "speciality": "Poda y mantenimiento general",
        "hire_date": "2020-03-15"
    },
    {
        "name": "Ana López",
        "phone": "645678901",
        "email": "ana@jardineria.com",
        "role": "Jardinera",
        "speciality": "Diseño floral y plantación",
        "hire_date": "2021-06-01"
    },
    {
        "name": "Pedro Sánchez",
        "phone": "656789012",
        "email": "pedro@jardineria.com",
        "role": "Jardinero",
        "speciality": "Sistemas de riego",
        "hire_date": "2022-09-10"
    },
]

# ── Tareas ─────────────────────────────────────────────────────
tareas = [
    {
        "title": "Mantenimiento jardín mensual",
        "description": "Poda de setos y revisión sistema de riego",
        "date": "2026-03-20",
        "start_time": "09:00:00",
        "end_time": "12:00:00",
        "status": "pendiente",
        "priority": "alta",
        "client_id": 1,
        "employee_ids": [1, 2],
        "notes": "Llevar tijeras de poda grandes"
    },
    {
        "title": "Instalación sistema de riego",
        "description": "Instalar riego por goteo en zona trasera",
        "date": "2026-03-21",
        "start_time": "08:00:00",
        "end_time": "14:00:00",
        "status": "pendiente",
        "priority": "media",
        "client_id": 2,
        "employee_ids": [3],
        "notes": "Confirmar medidas antes de ir"
    },
    {
        "title": "Limpieza zonas verdes nave industrial",
        "description": "Corte de césped y recogida de hojas",
        "date": "2026-03-22",
        "start_time": "07:00:00",
        "end_time": "11:00:00",
        "status": "pendiente",
        "priority": "baja",
        "client_id": 3,
        "employee_ids": [1, 3],
        "notes": "Acceso por puerta lateral"
    },
]


def seed():
    print("🌱 Iniciando carga de datos de prueba...\n")

    # Crear clientes
    print("👤 Creando clientes...")
    for c in clientes:
        r = requests.post(f"{BASE_URL}/clients/", json=c)
        if r.status_code == 201:
            print(f"   ✅ {c['name']}")
        else:
            print(f"   ❌ {c['name']} — {r.json()}")

    # Crear empleados
    print("\n👷 Creando empleados...")
    for e in empleados:
        r = requests.post(f"{BASE_URL}/employees/", json=e)
        if r.status_code == 201:
            print(f"   ✅ {e['name']}")
        else:
            print(f"   ❌ {e['name']} — {r.json()}")

    # Crear tareas
    print("\n📅 Creando tareas...")
    for t in tareas:
        r = requests.post(f"{BASE_URL}/tasks/", json=t)
        if r.status_code == 201:
            print(f"   ✅ {t['title']}")
        else:
            print(f"   ❌ {t['title']} — {r.json()}")

    print("\n🌿 Datos de prueba cargados correctamente.")


if __name__ == "__main__":
    seed()