"""
Tests del módulo de trabajos y checklists.
"""
import pytest
from datetime import date


@pytest.fixture
def setup_trabajo(client, cliente_ejemplo, empleado_ejemplo):
    """Crea cliente, empleado y tarea para tests de trabajos."""
    cli   = client.post("/clients/",   json=cliente_ejemplo).json()
    emp   = client.post("/employees/", json=empleado_ejemplo).json()
    tarea = client.post("/tasks/", json={
        "title":        "Tarea para trabajo",
        "date":         str(date.today()),
        "status":       "pendiente",
        "priority":     "media",
        "client_id":    cli["id"],
        "employee_ids": [emp["id"]],
    }).json()
    return cli, emp, tarea


class TestTrabajosCRUD:
    """Tests CRUD de trabajos."""

    def test_crear_trabajo(self, client, setup_trabajo):
        """Debe crear un trabajo vinculado a una tarea."""
        cli, emp, tarea = setup_trabajo
        r = client.post("/jobs/", json={
            "task_id": tarea["id"],
            "status":  "en_progreso",
            "notes":   "Trabajo iniciado",
        })
        assert r.status_code == 201
        data = r.json()
        assert data["task_id"] == tarea["id"]
        assert data["status"]  == "en_progreso"

    def test_crear_trabajo_tarea_inexistente(self, client):
        """Debe rechazar trabajos con tarea inexistente."""
        r = client.post("/jobs/", json={
            "task_id": 9999,
            "status":  "en_progreso",
        })
        assert r.status_code in [404, 422]

    def test_listar_trabajos(self, client, setup_trabajo):
        """Debe devolver lista de trabajos."""
        cli, emp, tarea = setup_trabajo
        client.post("/jobs/", json={"task_id": tarea["id"], "status": "en_progreso"})
        r = client.get("/jobs/")
        assert r.status_code == 200
        assert len(r.json()) >= 1

    def test_actualizar_estado_trabajo(self, client, setup_trabajo):
        """Debe actualizar el estado del trabajo."""
        cli, emp, tarea = setup_trabajo
        job = client.post("/jobs/", json={
            "task_id": tarea["id"],
            "status":  "en_progreso",
        }).json()
        r = client.put(f"/jobs/{job['id']}", json={"status": "completado"})
        assert r.status_code == 200
        assert r.json()["status"] == "completado"

    def test_añadir_checklist_item(self, client, setup_trabajo):
        """Debe añadir un ítem al checklist del trabajo."""
        cli, emp, tarea = setup_trabajo
        job = client.post("/jobs/", json={
            "task_id": tarea["id"],
            "status":  "en_progreso",
        }).json()
        r = client.post(f"/jobs/{job['id']}/checklist", json={
            "description": "Verificar riego",
            "is_done":     False,
        })
        assert r.status_code in [200, 201]
        data = r.json()
        items = data.get("checklist_items", [data] if "description" in data else [])
        descripciones = [i.get("description", "") for i in items]
        assert "Verificar riego" in descripciones

    def test_marcar_checklist_done(self, client, setup_trabajo):
        """Debe marcar un ítem del checklist como completado."""
        cli, emp, tarea = setup_trabajo
        job = client.post("/jobs/", json={
            "task_id": tarea["id"],
            "status":  "en_progreso",
        }).json()
        item = client.post(f"/jobs/{job['id']}/checklist", json={
            "description": "Verificar riego",
            "is_done":     False,
        }).json()
        r = client.patch(f"/jobs/checklist/{item['id']}", json={"is_done": True})
        assert r.status_code == 200
        assert r.json()["is_done"] is True

    def test_registrar_incidencia(self, client, setup_trabajo):
        """Debe registrar una incidencia en un ítem del checklist."""
        cli, emp, tarea = setup_trabajo
        job = client.post("/jobs/", json={
            "task_id": tarea["id"],
            "status":  "en_progreso",
        }).json()
        item = client.post(f"/jobs/{job['id']}/checklist", json={
            "description": "Revisar bomba de agua",
            "is_done":     False,
        }).json()
        r = client.patch(f"/jobs/checklist/{item['id']}", json={
            "has_incident":    True,
            "incident_notes":  "Bomba con fuga de agua",
        })
        assert r.status_code == 200
        assert r.json()["has_incident"]   is True
        assert "fuga" in r.json()["incident_notes"].lower()

    def test_trabajo_con_checklist_completo(self, client, setup_trabajo):
        """Debe crear trabajo con múltiples ítems en el checklist."""
        cli, emp, tarea = setup_trabajo
        job = client.post("/jobs/", json={
            "task_id":        tarea["id"],
            "status":         "en_progreso",
            "checklist_items": [
                {"description": "Paso 1", "is_done": False},
                {"description": "Paso 2", "is_done": False},
                {"description": "Paso 3", "is_done": False},
            ]
        }).json()
        assert job["task_id"] == tarea["id"]
        items = job.get("checklist_items", [])
        assert len(items) == 3