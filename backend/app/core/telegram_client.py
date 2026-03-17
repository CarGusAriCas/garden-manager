"""
Cliente Telegram para envío de mensajes al bot.
"""
import httpx
from app.core.config import settings


TELEGRAM_API = "https://api.telegram.org"


def send_telegram(chat_id: str, message: str, parse_mode: str = "HTML") -> dict:
    """
    Envía un mensaje de Telegram.

    Args:
        chat_id: ID del chat o canal destino
        message: Texto del mensaje (soporta HTML)
        parse_mode: 'HTML' o 'Markdown'

    Returns:
        Diccionario con ok y message_id

    Raises:
        Exception: Si el envío falla
    """
    if not settings.telegram_token:
        raise Exception("Telegram no configurado. Revisa TELEGRAM_TOKEN en .env")

    url      = f"{TELEGRAM_API}/bot{settings.telegram_token}/sendMessage"
    payload  = {
        "chat_id":    chat_id,
        "text":       message,
        "parse_mode": parse_mode,
    }

    response = httpx.post(url, json=payload, timeout=10)
    data     = response.json()

    if not data.get("ok"):
        raise Exception(f"Telegram error: {data.get('description', 'Unknown error')}")

    return {
        "ok":         True,
        "message_id": data["result"]["message_id"]
    }


def send_telegram_alert(message: str) -> dict:
    """
    Envía una alerta al chat_id configurado en .env.
    Útil para alertas del encargado.

    Args:
        message: Texto de la alerta

    Returns:
        Resultado del envío
    """
    return send_telegram(settings.telegram_chat_id, message)