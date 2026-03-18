"""
Cliente HTTP para comunicarse con la API de GardenManager.
Todas las llamadas al backend pasan por aquí.
"""
import httpx
import streamlit as st
from datetime import date
import os
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), "../../backend/.env"))

BASE_URL = os.getenv("API_URL", "http://localhost:8000")


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


def _patch(endpoint: str, data: dict) -> dict:
    """Petición PATCH genérica."""
    response = httpx.patch(f"{BASE_URL}{endpoint}", json=data)
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


def geocode_address(address: str):
    from geopy.geocoders import Nominatim
    from geopy.extra.rate_limiter import RateLimiter
    from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
    try:
        geolocator = Nominatim(
            user_agent="garden_manager_mlg",
            timeout=10                          # ← sube de 1 a 10 segundos
        )
        geocode = RateLimiter(
            geolocator.geocode,
            min_delay_seconds=1.1,              # ← respeta límite Nominatim
            max_retries=2,
            error_wait_seconds=3,               # ← espera 3s antes de reintentar
            swallow_exceptions=True             # ← no bloquea si falla uno
        )
        location = geocode(address)
        if location:
            return location.latitude, location.longitude
        return None, None
    except (GeocoderTimedOut, GeocoderUnavailable):
        return None, None

# ── Clientes ───────────────────────────────────────────────────

@st.cache_data(ttl=300)
def get_clients() -> list:
    return _get("/clients/")

@st.cache_data(ttl=30)
def get_client(client_id: int) -> dict:
    return _get(f"/clients/{client_id}")

def create_client(data: dict) -> dict:
    st.cache_data.clear()
    return _post("/clients/", data)

def update_client(client_id: int, data: dict) -> dict:
    st.cache_data.clear()
    return _put(f"/clients/{client_id}", data)

def delete_client(client_id: int) -> dict:
    st.cache_data.clear()
    return _delete(f"/clients/{client_id}")

def update_client_coordinates(client_id: int, lat: float, lon: float) -> dict:
    st.cache_data.clear()
    return _patch(
        f"/clients/{client_id}/coordinates?lat={lat}&lon={lon}", {}
    )


# ── Empleados ──────────────────────────────────────────────────

@st.cache_data(ttl=300)
def get_employees() -> list:
    """Lista de empleados — cacheada 30 segundos."""
    return _get("/employees/")

@st.cache_data(ttl=30)
def get_employee(employee_id: int) -> dict:
    return _get(f"/employees/{employee_id}")

def create_employee(data: dict) -> dict:
    st.cache_data.clear()
    return _post("/employees/", data)

def update_employee(employee_id: int, data: dict) -> dict:
    st.cache_data.clear()
    return _put(f"/employees/{employee_id}", data)

def delete_employee(employee_id: int) -> dict:
    st.cache_data.clear()
    return _delete(f"/employees/{employee_id}")

def update_employee_coordinates(employee_id: int, lat: float, lon: float) -> dict:
    st.cache_data.clear()
    return _patch(
        f"/employees/{employee_id}/coordinates?lat={lat}&lon={lon}", {}
    )


# ── Tareas ─────────────────────────────────────────────────────

@st.cache_data(ttl=60)
def get_tasks() -> list:
    """Lista de tareas — cacheada 15 segundos."""
    return _get("/tasks/")

@st.cache_data(ttl=15)
def get_task(task_id: int) -> dict:
    return _get(f"/tasks/{task_id}")

@st.cache_data(ttl=15)
def get_tasks_by_day(target_date: date) -> list:
    return _get(f"/tasks/agenda/day?date={parse_date_api(target_date)}")

@st.cache_data(ttl=15)
def get_tasks_by_week(start: date, end: date) -> list:
    return _get(f"/tasks/agenda/week?start_date={parse_date_api(start)}&end_date={parse_date_api(end)}")

def create_task(data: dict) -> dict:
    st.cache_data.clear()
    return _post("/tasks/", data)

def update_task(task_id: int, data: dict) -> dict:
    st.cache_data.clear()
    return _put(f"/tasks/{task_id}", data)

def delete_task(task_id: int) -> dict:
    st.cache_data.clear()
    return _delete(f"/tasks/{task_id}")


# ── Trabajos ───────────────────────────────────────────────────

@st.cache_data(ttl=60)
def get_jobs() -> list:
    """Lista de trabajos — cacheada 15 segundos."""
    return _get("/jobs/")

@st.cache_data(ttl=15)
def get_job(job_id: int) -> dict:
    return _get(f"/jobs/{job_id}")

def create_job(data: dict) -> dict:
    st.cache_data.clear()
    return _post("/jobs/", data)

def update_job(job_id: int, data: dict) -> dict:
    st.cache_data.clear()
    return _put(f"/jobs/{job_id}", data)

def update_checklist_item(item_id: int, data: dict) -> dict:
    st.cache_data.clear()
    return _patch(f"/jobs/checklist/{item_id}", data)


# ── Ausencias ──────────────────────────────────────────────────

@st.cache_data(ttl=120)
def get_absences() -> list:
    """Lista de ausencias — cacheada 30 segundos."""
    return _get("/absences/")

@st.cache_data(ttl=30)
def get_absences_by_employee(employee_id: int) -> list:
    return _get(f"/absences/by-employee/{employee_id}")

def create_absence(data: dict) -> dict:
    st.cache_data.clear()
    return _post("/absences/", data)

def update_absence(absence_id: int, data: dict) -> dict:
    st.cache_data.clear()
    return _put(f"/absences/{absence_id}", data)

def check_availability(employee_id: int, target_date: date) -> dict:
    return _get(f"/absences/check-availability/{employee_id}?date={parse_date_api(target_date)}")


# ── Autenticación ──────────────────────────────────────────────

def login(email: str, password: str) -> dict:
    """Autentica un usuario y devuelve el token JWT."""
    try:
        r = httpx.post(
            f"{BASE_URL}/auth/login",
            data={"username": email, "password": password},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=30
        )
        if r.status_code == 200:
            return {"ok": True, **r.json()}
        return {"ok": False, "error": r.json().get("detail", "Error de autenticación")}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def activate_account(token: str, new_password: str, confirm_password: str) -> dict:
    """Activa una cuenta con el token del email."""
    try:
        r = httpx.post(
            f"{BASE_URL}/auth/activate",
            json={"token": token, "new_password": new_password, "confirm_password": confirm_password},
            timeout=30
        )
        if r.status_code == 200:
            return {"ok": True, **r.json()}
        return {"ok": False, "error": r.json().get("detail", "Error")}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def request_password_reset(email: str) -> dict:
    """Solicita reset de contraseña."""
    try:
        r = httpx.post(
            f"{BASE_URL}/auth/reset-password/request",
            json={"email": email},
            timeout=30
        )
        return {"ok": True, "message": r.json().get("message", "")}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def confirm_password_reset(token: str, new_password: str, confirm_password: str) -> dict:
    """Confirma el reset de contraseña con el token del email."""
    try:
        r = httpx.post(
            f"{BASE_URL}/auth/reset-password/confirm",
            json={"token": token, "new_password": new_password, "confirm_password": confirm_password},
            timeout=30
        )
        if r.status_code == 200:
            return {"ok": True, **r.json()}
        return {"ok": False, "error": r.json().get("detail", "Error")}
    except Exception as e:
        return {"ok": False, "error": str(e)}
    

def solicitar_acceso(pagina: str, usuario: str, rol_actual: str) -> dict:
    """Envía solicitud de acceso al admin via Telegram."""
    try:
        import urllib.parse
        return _post(
            f"/notifications/solicitar-acceso"
            f"?usuario={urllib.parse.quote(usuario)}"
            f"&rol={urllib.parse.quote(rol_actual)}"
            f"&seccion={urllib.parse.quote(pagina)}",
            {}
        )
    except Exception as e:
        return {"ok": False, "error": str(e)}
    

def ping_backend() -> bool:
    """Despierta el backend si está dormido."""
    try:
        httpx.get(f"{BASE_URL}/ping", timeout=60)
        return True
    except Exception:
        return False