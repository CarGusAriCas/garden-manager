"""
Servicio unificado de notificaciones.
Gestiona el envío por WhatsApp (Twilio) y Telegram.
"""
from app.core.twilio_client import send_whatsapp
from app.core.telegram_client import send_telegram, send_telegram_alert
from app.core.config import settings


# ── Plantillas de mensajes ─────────────────────────────────────

def _msg_tarea_asignada(empleado: str, tarea: str, fecha: str, hora: str, direccion: str) -> str:
    return (
        f"🌿 *GardenManager*\n\n"
        f"Hola {empleado}, tienes una nueva tarea asignada:\n\n"
        f"📋 *{tarea}*\n"
        f"📅 {fecha} a las {hora}\n"
        f"📍 {direccion}\n\n"
        f"Consulta los detalles en la app."
    )

def _msg_tarea_urgente(empleado: str, tarea: str, fecha: str, direccion: str) -> str:
    return (
        f"🔴 *URGENTE - GardenManager*\n\n"
        f"Hola {empleado}, se ha asignado una tarea URGENTE:\n\n"
        f"📋 *{tarea}*\n"
        f"📅 {fecha}\n"
        f"📍 {direccion}\n\n"
        f"Por favor confirma disponibilidad."
    )

def _msg_recordatorio(empleado: str, tareas: list, fecha: str) -> str:
    lista = "\n".join([f"  • {t}" for t in tareas])
    return (
        f"🌿 *GardenManager - Recordatorio*\n\n"
        f"Hola {empleado}, mañana {fecha} tienes:\n\n"
        f"{lista}\n\n"
        f"¡Hasta mañana!"
    )

def _msg_trabajo_completado(cliente: str, tarea: str, fecha: str) -> str:
    return (
        f"🌿 *GardenManager*\n\n"
        f"Estimado/a {cliente},\n\n"
        f"Le informamos que el servicio *{tarea}* "
        f"programado para el {fecha} ha sido completado.\n\n"
        f"Gracias por confiar en nosotros."
    )

def _msg_incidencia(tarea: str, descripcion: str) -> str:
    return (
        f"🚨 *Incidencia detectada - GardenManager*\n\n"
        f"Tarea: *{tarea}*\n\n"
        f"📝 {descripcion}\n\n"
        f"Revisa el trabajo en la app para más detalles."
    )

def _msg_ausencia_aprobada(empleado: str, inicio: str, fin: str) -> str:
    return (
        f"🌿 *GardenManager*\n\n"
        f"Hola {empleado},\n\n"
        f"Tu solicitud de ausencia del {inicio} al {fin} "
        f"ha sido ✅ *APROBADA*.\n\n"
        f"¡Disfruta tu descanso!"
    )

def _msg_ausencia_denegada(empleado: str, inicio: str, fin: str, motivo: str = "") -> str:
    return (
        f"🌿 *GardenManager*\n\n"
        f"Hola {empleado},\n\n"
        f"Tu solicitud de ausencia del {inicio} al {fin} "
        f"ha sido ❌ *DENEGADA*.\n\n"
        f"{f'Motivo: {motivo}' if motivo else 'Contacta con tu encargado para más información.'}"
    )


# ── Funciones de envío ─────────────────────────────────────────

def notificar_tarea_asignada(
    empleado_nombre: str,
    empleado_whatsapp: str,
    empleado_telegram: str,
    tarea_titulo: str,
    fecha: str,
    hora: str,
    direccion: str,
    urgente: bool = False
) -> dict:
    """
    Notifica a un empleado que se le ha asignado una tarea.

    Returns:
        Diccionario con resultado de cada canal
    """
    resultados = {}

    if urgente:
        mensaje = _msg_tarea_urgente(empleado_nombre, tarea_titulo, fecha, direccion)
    else:
        mensaje = _msg_tarea_asignada(empleado_nombre, tarea_titulo, fecha, hora, direccion)

    # WhatsApp
    if empleado_whatsapp:
        try:
            resultados["whatsapp"] = send_whatsapp(empleado_whatsapp, mensaje)
        except Exception as e:
            resultados["whatsapp"] = {"error": str(e)}

    # Telegram
    if empleado_telegram:
        try:
            resultados["telegram"] = send_telegram(empleado_telegram, mensaje)
        except Exception as e:
            resultados["telegram"] = {"error": str(e)}

    return resultados


def notificar_trabajo_completado(
    cliente_nombre: str,
    cliente_whatsapp: str,
    tarea_titulo: str,
    fecha: str
) -> dict:
    """Notifica al cliente que su trabajo ha sido completado."""
    resultados = {}
    mensaje    = _msg_trabajo_completado(cliente_nombre, tarea_titulo, fecha)

    if cliente_whatsapp:
        try:
            resultados["whatsapp"] = send_whatsapp(cliente_whatsapp, mensaje)
        except Exception as e:
            resultados["whatsapp"] = {"error": str(e)}

    return resultados


def notificar_incidencia(
    tarea_titulo: str,
    descripcion: str,
    telegram_encargado: str = None
) -> dict:
    """
    Notifica una incidencia al encargado via Telegram.
    Usa el chat_id del .env si no se especifica otro.
    """
    resultados = {}
    mensaje    = _msg_incidencia(tarea_titulo, descripcion)
    chat_id    = telegram_encargado or settings.telegram_chat_id

    if chat_id:
        try:
            resultados["telegram"] = send_telegram(chat_id, mensaje)
        except Exception as e:
            resultados["telegram"] = {"error": str(e)}

    return resultados


def notificar_ausencia(
    empleado_nombre: str,
    empleado_whatsapp: str,
    empleado_telegram: str,
    inicio: str,
    fin: str,
    aprobada: bool,
    motivo: str = ""
) -> dict:
    """Notifica al empleado el resultado de su solicitud de ausencia."""
    resultados = {}

    if aprobada:
        mensaje = _msg_ausencia_aprobada(empleado_nombre, inicio, fin)
    else:
        mensaje = _msg_ausencia_denegada(empleado_nombre, inicio, fin, motivo)

    if empleado_whatsapp:
        try:
            resultados["whatsapp"] = send_whatsapp(empleado_whatsapp, mensaje)
        except Exception as e:
            resultados["whatsapp"] = {"error": str(e)}

    if empleado_telegram:
        try:
            resultados["telegram"] = send_telegram(empleado_telegram, mensaje)
        except Exception as e:
            resultados["telegram"] = {"error": str(e)}

    return resultados


def notificar_recordatorio(
    empleado_nombre: str,
    empleado_whatsapp: str,
    empleado_telegram: str,
    tareas: list,
    fecha: str
) -> dict:
    """Envía recordatorio de tareas del día siguiente."""
    resultados = {}
    mensaje    = _msg_recordatorio(empleado_nombre, tareas, fecha)

    if empleado_whatsapp:
        try:
            resultados["whatsapp"] = send_whatsapp(empleado_whatsapp, mensaje)
        except Exception as e:
            resultados["whatsapp"] = {"error": str(e)}

    if empleado_telegram:
        try:
            resultados["telegram"] = send_telegram(empleado_telegram, mensaje)
        except Exception as e:
            resultados["telegram"] = {"error": str(e)}

    return resultados