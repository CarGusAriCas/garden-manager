"""
Tests del módulo de empleados.
"""
import pytest


class TestEmpleadosCRUD:
    """Tests CRUD de empleados."""

    def test_crear_empleado(self, client, empleado_ejemplo):
        """Debe crear un empleado y devolver 201."""
        r = client.post("/employees/", json=empleado_ejemplo)
        assert r.status_code == 201
        data = r.json()
        assert data["name"] == empleado_ejemplo["name"]
        assert data["role"] == empleado_ejemplo["role"]

    def test_crear_empleado_email_duplicado(self, client, empleado_ejemplo):
        """Debe rechazar emails duplicados."""
        client.post("/employees/", json=empleado_ejemplo)
        r = client.post("/employees/", json=empleado_ejemplo)
        assert r.status_code == 400

    def test_listar_empleados(self, client, empleado_ejemplo):
        """Debe devolver lista de empleados activos."""
        client.post("/employees/", json=empleado_ejemplo)
        r = client.get("/employees/")
        assert r.status_code == 200
        assert len(r.json()) >= 1

    def test_empleados_disponibles(self, client, empleado_ejemplo):
        """Debe devolver empleados disponibles."""
        client.post("/employees/", json=empleado_ejemplo)
        r = client.get("/employees/available")
        assert r.status_code == 200
        assert len(r.json()) >= 1

    def test_obtener_empleado_por_id(self, client, empleado_ejemplo):
        """Debe devolver el empleado correcto por ID."""
        creado = client.post("/employees/", json=empleado_ejemplo).json()
        r      = client.get(f"/employees/{creado['id']}")
        assert r.status_code == 200
        assert r.json()["name"] == empleado_ejemplo["name"]

    def test_actualizar_empleado(self, client, empleado_ejemplo):
        """Debe actualizar los campos enviados."""
        creado = client.post("/employees/", json=empleado_ejemplo).json()
        r      = client.put(
            f"/employees/{creado['id']}",
            json={"role": "Encargado"}
        )
        assert r.status_code == 200
        assert r.json()["role"] == "Encargado"

    def test_desactivar_empleado(self, client, empleado_ejemplo):
        """Debe desactivar el empleado (borrado lógico)."""
        creado = client.post("/employees/", json=empleado_ejemplo).json()
        r      = client.delete(f"/employees/{creado['id']}")
        assert r.status_code == 200
        lista  = client.get("/employees/").json()
        assert all(e["id"] != creado["id"] for e in lista)