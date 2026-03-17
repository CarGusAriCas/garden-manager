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
    app_name: str = "GardenManager"
    app_version: str = "0.1.0"
    debug: bool = True
    database_url: str = "sqlite:///./database/garden_manager.db"

    # GitHub
    github_token: str = ""
    github_repo:  str = "CarGusAriCas/garden-manager"

    class Config:
        env_file = ".env"


# Instancia única que usaremos en toda la aplicación
settings = Settings()