"""
Tests del módulo de clientes.
Verifica los endpoints CRUD completos.
"""
import pytest


class TestClientesCRUD:
    """Tests de creación, lectura, actualización y borrado de clientes."""

    def test_crear_cliente(self, client, cliente_ejemplo):
        """Debe crear un cliente y devolver 201."""
        r = client.post("/clients/", json=cliente_ejemplo)
        assert r.status_code == 201
        data = r.json()
        assert data["name"]  == cliente_ejemplo["name"]
        assert data["email"] == cliente_ejemplo["email"]
        assert data["is_active"] is True
        assert "id" in data

    def test_crear_cliente_sin_nombre(self, client):
        """Debe rechazar la creación sin nombre obligatorio."""
        r = client.post("/clients/", json={"email": "test@test.com"})
        assert r.status_code == 422

    def test_crear_cliente_email_duplicado(self, client, cliente_ejemplo):
        """Debe rechazar emails duplicados."""
        client.post("/clients/", json=cliente_ejemplo)
        r = client.post("/clients/", json=cliente_ejemplo)
        assert r.status_code == 400
        assert "email" in r.json()["detail"].lower()

    def test_listar_clientes(self, client, cliente_ejemplo):
        """Debe devolver lista de clientes activos."""
        client.post("/clients/", json=cliente_ejemplo)
        r = client.get("/clients/")
        assert r.status_code == 200
        assert len(r.json()) == 1

    def test_obtener_cliente_por_id(self, client, cliente_ejemplo):
        """Debe devolver el cliente correcto por ID."""
        creado = client.post("/clients/", json=cliente_ejemplo).json()
        r      = client.get(f"/clients/{creado['id']}")
        assert r.status_code == 200
        assert r.json()["name"] == cliente_ejemplo["name"]

    def test_obtener_cliente_inexistente(self, client):
        """Debe devolver 404 para ID inexistente."""
        r = client.get("/clients/9999")
        assert r.status_code == 404

    def test_actualizar_cliente(self, client, cliente_ejemplo):
        """Debe actualizar los campos enviados."""
        creado = client.post("/clients/", json=cliente_ejemplo).json()
        r      = client.put(
            f"/clients/{creado['id']}",
            json={"name": "Nombre Actualizado"}
        )
        assert r.status_code == 200
        assert r.json()["name"] == "Nombre Actualizado"

    def test_desactivar_cliente(self, client, cliente_ejemplo):
        """Debe desactivar el cliente (borrado lógico)."""
        creado = client.post("/clients/", json=cliente_ejemplo).json()
        r      = client.delete(f"/clients/{creado['id']}")
        assert r.status_code == 200

        # El cliente no debe aparecer en la lista
        lista = client.get("/clients/").json()
        assert len(lista) == 0

    def test_cliente_desactivado_no_aparece(self, client, cliente_ejemplo):
        """Los clientes desactivados no deben aparecer en el listado."""
        creado = client.post("/clients/", json=cliente_ejemplo).json()
        client.delete(f"/clients/{creado['id']}")
        r = client.get("/clients/")
        assert all(c["id"] != creado["id"] for c in r.json())