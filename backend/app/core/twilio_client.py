"""
Cliente Twilio para envío de mensajes WhatsApp.
Usa el sandbox de Twilio para desarrollo.
"""
from twilio.rest import Client
from app.core.config import settings


def get_twilio_client() -> Client:
    """Devuelve una instancia del cliente Twilio."""
    return Client(settings.twilio_account_sid, settings.twilio_auth_token)


def send_whatsapp(to: str, message: str) -> dict:
    """
    Envía un mensaje de WhatsApp via Twilio.

    Args:
        to: Número destino en formato +34612345678
        message: Texto del mensaje

    Returns:
        Diccionario con sid y status del mensaje

    Raises:
        Exception: Si el envío falla
    """
    if not settings.twilio_account_sid:
        raise Exception("Twilio no configurado. Revisa TWILIO_ACCOUNT_SID en .env")

    # Formatea el número destino
    if not to.startswith("whatsapp:"):
        to = f"whatsapp:{to}"

    client = get_twilio_client()
    msg    = client.messages.create(
        from_=settings.twilio_whatsapp_from,
        to=to,
        body=message
    )
    return {"sid": msg.sid, "status": msg.status}


def send_whatsapp_template(to: str, template_sid: str, variables: dict) -> dict:
    """
    Envía un mensaje usando una plantilla aprobada de Twilio.
    Necesario para iniciar conversaciones (Business-Initiated).

    Args:
        to: Número destino
        template_sid: SID de la plantilla
        variables: Variables de la plantilla

    Returns:
        Diccionario con sid y status
    """
    if not to.startswith("whatsapp:"):
        to = f"whatsapp:{to}"

    client = get_twilio_client()
    msg    = client.messages.create(
        from_=settings.twilio_whatsapp_from,
        to=to,
        content_sid=template_sid,
        content_variables=str(variables)
    )
    return {"sid": msg.sid, "status": msg.status}