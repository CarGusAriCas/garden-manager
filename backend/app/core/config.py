"""
Configuración central de la aplicación.
Lee las variables de entorno desde el archivo .env
"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Configuración de la aplicación.
    Los valores se cargan automáticamente desde el archivo .env
    """
    app_name:     str = "GardenManager"
    app_version:  str = "0.1.0"
    debug:        bool = True
    database_url: str = "sqlite:///./database/garden_manager.db"

    # GitHub
    github_token: str = ""
    github_repo:  str = "CarGusAriCas/garden-manager"

    # API
    api_url: str = "http://localhost:8000"

    # Twilio WhatsApp
    twilio_account_sid:   str = "ACdbc0c7d072a76df4c0d91748bd0e38a0"
    twilio_auth_token:    str = "be042c45da594ac22cb67e92da26e397"
    twilio_whatsapp_from: str = "whatsapp:+14155238886"

    # Telegram
    telegram_token:   str = ""
    telegram_chat_id: str = ""
    class Config:
        env_file = ".env"


# Instancia única que usaremos en toda la aplicación
settings = Settings()