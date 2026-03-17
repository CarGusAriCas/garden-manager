"""
Configuración central de la aplicación.
Lee las variables de entorno desde el archivo .env
"""
from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Configuración de la aplicación.
    Los valores se cargan automáticamente desde el archivo .env
    """
    model_config = ConfigDict(env_file=".env")
    app_name:     str = "GardenManager"
    app_version:  str = "0.1.0"
    debug:        bool = True
    database_url: str = "sqlite:///./database/garden_manager.db"

    # GitHub
    github_token: str = ""
    github_repo:  str = ""

    # API
    api_url: str = "http://localhost:8000"

    # Twilio WhatsApp
    twilio_account_sid:   str = ""
    twilio_auth_token:    str = ""
    twilio_whatsapp_from: str = ""

    # Telegram
    telegram_token:   str = ""
    telegram_chat_id: str = ""

# Instancia única que usaremos en toda la aplicación
settings = Settings()