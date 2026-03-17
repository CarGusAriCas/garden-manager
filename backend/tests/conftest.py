"""
Configuración global de tests.
Crea una BD en memoria para cada test — no toca la BD real.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.core.database import Base, get_db

TEST_DATABASE_URL = "sqlite:///./test.db"

engine_test = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine_test
)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function", autouse=False)
def client():
    """
    Cliente de test con BD limpia para cada test.
    """
    # Crea tablas
    Base.metadata.create_all(bind=engine_test)
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    # Limpia después de cada test
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine_test)


@pytest.fixture
def cliente_ejemplo():
    return {
        "name":    "Test Cliente",
        "phone":   "612000001",
        "email":   "test@ejemplo.com",
        "address": "Calle Test 1, Málaga",
        "notes":   "Cliente de prueba"
    }


@pytest.fixture
def empleado_ejemplo():
    return {
        "name":       "Test Empleado",
        "phone":      "623000001",
        "email":      "empleado@test.com",
        "role":       "Jardinero",
        "speciality": "Poda",
        "hire_date":  "2024-01-01"
    }


@pytest.fixture
def setup_tarea(client, cliente_ejemplo, empleado_ejemplo):
    """Crea cliente y empleado para tests de tareas."""
    cli = client.post("/clients/",   json=cliente_ejemplo).json()
    emp = client.post("/employees/", json=empleado_ejemplo).json()
    return cli, emp