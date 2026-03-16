"""
Cliente HTTP para comunicarse con la API de GardenManager.
Todas las llamadas al backend pasan por aquí.
"""
import httpx
from datetime import date

BASE_URL = "http://localhost:8000"


def _get(endpoint: str) -> dict | list:
    """Petición GET genérica."""
    response = httpx.get(f"{BASE_URL}{endpoint}")
    response.raise_for_status()
    return response.json()


def _post(endpoint: str, data: dict) -> dict:
    """Petición POST genérica."""
    response = httpx.post(f"{BASE_URL}{endpoint}", json=data)
    response.raise_for_status()
    return response.json()


def _put(endpoint: str, data: dict) -> dict:
    """Petición PUT genérica."""
    response = httpx.put(f"{BASE_URL}{endpoint}", json=data)
    response.raise_for_status()
    return response.json()


def _delete(endpoint: str) -> dict:
    """Petición DELETE genérica."""
    response = httpx.delete(f"{BASE_URL}{endpoint}")
    response.raise_for_status()
    return response.json()


# ── Utilidades de fecha ────────────────────────────────────────

def format_date_es(date_str: str) -> str:
    """Convierte YYYY-MM-DD a DD/MM/YYYY para mostrar al usuario."""
    if not date_str:
        return ""
    from datetime import datetime
    d = datetime.strptime(date_str[:10], "%Y-%m-%d")
    return d.strftime("%d/%m/%Y")


def parse_date_api(d: date) -> str:
    """Convierte objeto date a YYYY-MM-DD para enviar a la API."""
    return d.strftime("%Y-%m-%d")


# ── Clientes ───────────────────────────────────────────────────

def get_clients() -> list:
    return _get("/clients/")

def get_client(client_id: int) -> dict:
    return _get(f"/clients/{client_id}")

def create_client(data: dict) -> dict:
    return _post("/clients/", data)

def update_client(client_id: int, data: dict) -> dict:
    return _put(f"/clients/{client_id}", data)

def delete_client(client_id: int) -> dict:
    return _delete(f"/clients/{client_id}")


# ── Empleados ──────────────────────────────────────────────────

def get_employees() -> list:
    return _get("/employees/")

def get_employee(employee_id: int) -> dict:
    return _get(f"/employees/{employee_id}")

def create_employee(data: dict) -> dict:
    return _post("/employees/", data)

def update_employee(employee_id: int, data: dict) -> dict:
    return _put(f"/employees/{employee_id}", data)

def delete_employee(employee_id: int) -> dict:
    return _delete(f"/employees/{employee_id}")


# ── Tareas ─────────────────────────────────────────────────────

def get_tasks() -> list:
    return _get("/tasks/")

def get_task(task_id: int) -> dict:
    return _get(f"/tasks/{task_id}")

def get_tasks_by_day(target_date: date) -> list:
    return _get(f"/tasks/agenda/day?date={parse_date_api(target_date)}")

def get_tasks_by_week(start: date, end: date) -> list:
    return _get(f"/tasks/agenda/week?start_date={parse_date_api(start)}&end_date={parse_date_api(end)}")

def create_task(data: dict) -> dict:
    return _post("/tasks/", data)

def update_task(task_id: int, data: dict) -> dict:
    return _put(f"/tasks/{task_id}", data)

def delete_task(task_id: int) -> dict:
    return _delete(f"/tasks/{task_id}")


# ── Trabajos ───────────────────────────────────────────────────

def get_jobs() -> list:
    return _get("/jobs/")

def get_job(job_id: int) -> dict:
    return _get(f"/jobs/{job_id}")

def create_job(data: dict) -> dict:
    return _post("/jobs/", data)

def update_job(job_id: int, data: dict) -> dict:
    return _put(f"/jobs/{job_id}", data)

def update_checklist_item(item_id: int, data: dict) -> dict:
    return _put(f"/jobs/checklist/{item_id}", data)


# ── Ausencias ──────────────────────────────────────────────────

def get_absences() -> list:
    return _get("/absences/")

def get_absences_by_employee(employee_id: int) -> list:
    return _get(f"/absences/by-employee/{employee_id}")

def create_absence(data: dict) -> dict:
    return _post("/absences/", data)

def update_absence(absence_id: int, data: dict) -> dict:
    return _put(f"/absences/{absence_id}", data)

def check_availability(employee_id: int, target_date: date) -> dict:
    return _get(f"/absences/check-availability/{employee_id}?date={parse_date_api(target_date)}")