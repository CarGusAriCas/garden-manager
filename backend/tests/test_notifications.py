"""
Tests del módulo de notificaciones.
Verifica que los endpoints responden correctamente sin enviar mensajes reales.
"""
from unittest.mock import patch


class TestNotificaciones:
    """Tests de los endpoints de notificaciones."""

    def test_test_telegram_endpoint_existe(self, client):
        """El endpoint de test Telegram debe existir."""
        with patch("app.core.telegram_client.send_telegram_alert", return_value={"ok": True}):
            r = client.post("/notifications/test-telegram")
            assert r.status_code == 200

    def test_mensaje_libre_sin_destinatario(self, client):
        """Debe rechazar mensaje sin destinatario."""
        r = client.post("/notifications/mensaje-libre", json={
            "mensaje": "Test mensaje",
        })
        assert r.status_code == 400

    def test_mensaje_libre_con_telegram(self, client):
        """Debe enviar mensaje con destinatario Telegram."""
        with patch("app.core.telegram_client.send_telegram_alert", return_value={"ok": True}):
            r = client.post("/notifications/mensaje-libre", json={
                "mensaje":                "Test mensaje",
                "destinatario_telegram":  "123456789",
            })
            assert r.status_code == 200

    def test_notificacion_tarea_asignada(self, client):
        """Debe procesar notificación de tarea asignada."""
        with patch("app.services.notification_service.notificar_tarea_asignada", return_value={"ok": True}):
            r = client.post("/notifications/tarea-asignada", json={
                "empleado_nombre":   "Test Empleado",
                "empleado_telegram": "123456789",
                "tarea_titulo":      "Test Tarea",
                "fecha":             "18/03/2026",
                "hora":              "09:00",
                "direccion":         "Calle Test 1",
                "urgente":           False,
            })
            assert r.status_code == 200

    def test_notificacion_ausencia_aprobada(self, client):
        """Debe procesar notificación de ausencia aprobada."""
        with patch("app.services.notification_service.notificar_ausencia", return_value={"ok": True}):
            r = client.post("/notifications/ausencia", json={
                "empleado_nombre":   "Test Empleado",
                "empleado_telegram": "123456789",
                "inicio":            "01/07/2026",
                "fin":               "14/07/2026",
                "aprobada":          True,
                "motivo":            "",
            })
            assert r.status_code == 200

    def test_notificacion_recordatorio(self, client):
        """Debe procesar recordatorio de tareas."""
        with patch("app.services.notification_service.notificar_recordatorio", return_value={"ok": True}):
            r = client.post("/notifications/recordatorio", json={
                "empleado_nombre":   "Test Empleado",
                "empleado_telegram": "123456789",
                "tareas":            ["Tarea 1", "Tarea 2"],
                "fecha":             "19/03/2026",
            })
            assert r.status_code == 200