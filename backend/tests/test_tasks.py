"""
Tests del módulo de tareas.
"""
from datetime import date, timedelta


class TestTareasCRUD:
    """Tests CRUD de tareas."""

    def test_crear_tarea(self, client, setup_tarea):
        """Debe crear una tarea con cliente y empleado asignado."""
        cli, emp = setup_tarea
        tarea = {
            "title":        "Test tarea",
            "date":         str(date.today()),
            "status":       "pendiente",
            "priority":     "media",
            "client_id":    cli["id"],
            "employee_ids": [emp["id"]],
        }
        r = client.post("/tasks/", json=tarea)
        assert r.status_code == 201
        data = r.json()
        assert data["title"]             == "Test tarea"
        assert data["client"]["id"]      == cli["id"]
        assert len(data["employees"])    == 1

    def test_crear_tarea_cliente_inexistente(self, client):
        """Debe rechazar tareas con cliente inexistente."""
        r = client.post("/tasks/", json={
            "title":     "Test",
            "date":      str(date.today()),
            "status":    "pendiente",
            "priority":  "media",
            "client_id": 9999,
        })
        assert r.status_code in [404]

    def test_agenda_dia(self, client, setup_tarea):
        """Debe devolver tareas de un día concreto."""
        cli, emp = setup_tarea
        hoy = str(date.today())
        r_create = client.post("/tasks/", json={
            "title":        "Tarea hoy",
            "date":         hoy,
            "status":       "pendiente",
            "priority":     "alta",
            "client_id":    cli["id"],
            "employee_ids": [emp["id"]],
        })
        assert r_create.status_code == 201
        r = client.get(f"/tasks/agenda/day?date={hoy}")
        assert r.status_code == 200
        titulos = [t["title"] for t in r.json()]
        assert "Tarea hoy" in titulos

    def test_agenda_semana(self, client, setup_tarea):
        """Debe devolver tareas de una semana."""
        cli, emp = setup_tarea
        hoy   = date.today()
        lunes = hoy - timedelta(days=hoy.weekday())
        r_create = client.post("/tasks/", json={
            "title":        "Tarea semana",
            "date":         str(lunes),
            "status":       "pendiente",
            "priority":     "baja",
            "client_id":    cli["id"],
            "employee_ids": [emp["id"]],
        })
        assert r_create.status_code == 201
        r = client.get(
            f"/tasks/agenda/week"
            f"?start_date={lunes}"
            f"&end_date={lunes + timedelta(days=6)}"
        )
        assert r.status_code == 200
        titulos = [t["title"] for t in r.json()]
        assert "Tarea semana" in titulos

    def test_actualizar_estado_tarea(self, client, setup_tarea):
        """Debe actualizar el estado de una tarea."""
        cli, emp = setup_tarea
        creada = client.post("/tasks/", json={
            "title":     "Tarea estado",
            "date":      str(date.today()),
            "status":    "pendiente",
            "priority":  "media",
            "client_id": cli["id"],
        }).json()
        r = client.put(
            f"/tasks/{creada['id']}",
            json={"status": "completada"}
        )
        assert r.status_code == 200
        assert r.json()["status"] == "completada"


    class TestAusencias:
        """Tests del módulo de ausencias."""

    def test_crear_ausencia(self, client, empleado_ejemplo):
        """Debe crear una ausencia para un empleado."""
        emp = client.post("/employees/", json=empleado_ejemplo).json()
        r   = client.post("/absences/", json={
            "employee_id":  emp["id"],
            "absence_type": "vacaciones",
            "start_date":   "2026-07-01",
            "end_date":     "2026-07-14",
            "reason":       "Vacaciones de verano"
        })
        assert r.status_code == 201
        assert r.json()["employee"]["id"] == emp["id"]

    def test_ausencia_fechas_invalidas(self, client, empleado_ejemplo):
        """Debe rechazar ausencias con fecha fin anterior a inicio."""
        emp = client.post("/employees/", json=empleado_ejemplo).json()
        r   = client.post("/absences/", json={
            "employee_id":  emp["id"],
            "absence_type": "vacaciones",
            "start_date":   "2026-07-14",
            "end_date":     "2026-07-01",
        })
        assert r.status_code == 422

    def test_disponibilidad_empleado(self, client, empleado_ejemplo):
        """Empleado con ausencia aprobada debe aparecer como no disponible."""
        emp = client.post("/employees/", json=empleado_ejemplo).json()
        aus = client.post("/absences/", json={
            "employee_id":  emp["id"],
            "absence_type": "vacaciones",
            "start_date":   "2026-07-01",
            "end_date":     "2026-07-14",
        }).json()

        # Aprueba la ausencia
        client.put(f"/absences/{aus['id']}", json={"is_approved": True})

        # Comprueba disponibilidad en fecha dentro del rango
        r = client.get(
            f"/absences/check-availability/{emp['id']}"
            f"?date=2026-07-07"
        )
        assert r.status_code == 200
        assert r.json()["available"] is False

        # Comprueba disponibilidad fuera del rango
        r2 = client.get(
            f"/absences/check-availability/{emp['id']}"
            f"?date=2026-08-01"
        )
        assert r2.json()["available"] is True