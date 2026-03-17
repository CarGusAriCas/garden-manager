"""
Router de notificaciones.
Endpoints para envío manual de mensajes via WhatsApp y Telegram.
"""
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Optional
from app.services.notification_service import (
    notificar_tarea_asignada,
    notificar_trabajo_completado,
    notificar_incidencia,
    notificar_ausencia,
    notificar_recordatorio,
)
from app.core.telegram_client import send_telegram_alert
from app.core.twilio_client import send_whatsapp

router = APIRouter(
    prefix="/notifications",
    tags=["Notificaciones"]
)


class MensajeLibre(BaseModel):
    """Schema para mensaje libre."""
    destinatario_whatsapp: Optional[str] = None
    destinatario_telegram: Optional[str] = None
    mensaje:               str


class NotificacionTarea(BaseModel):
    """Schema para notificación de tarea."""
    empleado_nombre:   str
    empleado_whatsapp: Optional[str] = None
    empleado_telegram: Optional[str] = None
    tarea_titulo:      str
    fecha:             str
    hora:              str = "09:00"
    direccion:         str = ""
    urgente:           bool = False


class NotificacionAusencia(BaseModel):
    """Schema para notificación de ausencia."""
    empleado_nombre:   str
    empleado_whatsapp: Optional[str] = None
    empleado_telegram: Optional[str] = None
    inicio:            str
    fin:               str
    aprobada:          bool
    motivo:            str = ""


class NotificacionTrabajo(BaseModel):
    """Schema para notificación de trabajo completado."""
    cliente_nombre:   str
    cliente_whatsapp: Optional[str] = None
    tarea_titulo:     str
    fecha:            str


class NotificacionIncidencia(BaseModel):
    """Schema para notificación de incidencia."""
    tarea_titulo:       str
    descripcion:        str
    telegram_encargado: Optional[str] = None

class NotificacionRecordatorio(BaseModel):
    """Schema para recordatorio de tareas."""
    empleado_nombre:   str
    empleado_whatsapp: Optional[str] = None
    empleado_telegram: Optional[str] = None
    tareas:            list[str]
    fecha:             str

@router.post("/mensaje-libre")
def enviar_mensaje_libre(data: MensajeLibre):
    """Envía un mensaje libre a WhatsApp y/o Telegram."""
    resultados = {}

    if not data.destinatario_whatsapp and not data.destinatario_telegram:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debes especificar al menos un destinatario"
        )

    if data.destinatario_whatsapp:
        try:
            resultados["whatsapp"] = send_whatsapp(
                data.destinatario_whatsapp, data.mensaje
            )
        except Exception as e:
            resultados["whatsapp"] = {"error": str(e)}

    if data.destinatario_telegram:
        try:
            resultados["telegram"] = send_telegram_alert(data.mensaje)
        except Exception as e:
            resultados["telegram"] = {"error": str(e)}

    return resultados


@router.post("/tarea-asignada")
def enviar_notificacion_tarea(data: NotificacionTarea):
    """Notifica a un empleado sobre una tarea asignada."""
    return notificar_tarea_asignada(
        empleado_nombre=data.empleado_nombre,
        empleado_whatsapp=data.empleado_whatsapp,
        empleado_telegram=data.empleado_telegram,
        tarea_titulo=data.tarea_titulo,
        fecha=data.fecha,
        hora=data.hora,
        direccion=data.direccion,
        urgente=data.urgente,
    )


@router.post("/trabajo-completado")
def enviar_notificacion_trabajo(data: NotificacionTrabajo):
    """Notifica al cliente que su trabajo ha sido completado."""
    return notificar_trabajo_completado(
        cliente_nombre=data.cliente_nombre,
        cliente_whatsapp=data.cliente_whatsapp,
        tarea_titulo=data.tarea_titulo,
        fecha=data.fecha,
    )


@router.post("/incidencia")
def enviar_notificacion_incidencia(data: NotificacionIncidencia):
    """Notifica una incidencia al encargado."""
    return notificar_incidencia(
        tarea_titulo=data.tarea_titulo,
        descripcion=data.descripcion,
        telegram_encargado=data.telegram_encargado,
    )


@router.post("/ausencia")
def enviar_notificacion_ausencia(data: NotificacionAusencia):
    """Notifica al empleado el resultado de su solicitud de ausencia."""
    return notificar_ausencia(
        empleado_nombre=data.empleado_nombre,
        empleado_whatsapp=data.empleado_whatsapp,
        empleado_telegram=data.empleado_telegram,
        inicio=data.inicio,
        fin=data.fin,
        aprobada=data.aprobada,
        motivo=data.motivo,
    )


@router.post("/test-telegram")
def test_telegram():
    """Endpoint de prueba para verificar la conexión con Telegram."""
    try:
        resultado = send_telegram_alert(
            "🌿 <b>GardenManager</b>\n\n"
            "✅ Conexión con Telegram funcionando correctamente."
        )
        return {"ok": True, "resultado": resultado}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/test-whatsapp")
def test_whatsapp(numero: str):
    """Endpoint de prueba para verificar la conexión con WhatsApp."""
    try:
        resultado = send_whatsapp(
            numero,
            "🌿 *GardenManager*\n\n"
            "✅ Conexión con WhatsApp funcionando correctamente."
        )
        return {"ok": True, "resultado": resultado}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/recordatorio")
def enviar_recordatorio(data: NotificacionRecordatorio):
    """
    Envía un recordatorio de tareas del día siguiente a un empleado.
    Ideal para ejecutar cada tarde-noche de forma automática.
    """
    return notificar_recordatorio(
        empleado_nombre=data.empleado_nombre,
        empleado_whatsapp=data.empleado_whatsapp,
        empleado_telegram=data.empleado_telegram,
        tareas=data.tareas,
        fecha=data.fecha,
    )