"""
Configuración de la conexión a la base de datos.
Usando SQLAlchemy como ORM, lo que nos permite cambiar
de SQLite a PostgreSQL solo modificando DATABASE_URL en .env
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.core.config import settings


# Motor de base de datos
# check_same_thread solo es necesario para SQLite
if settings.database_url.startswith("sqlite"):
    engine = create_engine(
        settings.database_url,
        connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(settings.database_url)

# Fábrica de sesiones: cada petición HTTP abrirá una sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """
    Clase base de la que heredarán todos los modelos.
    SQLAlchemy usará esta clase para crear las tablas.
    """
    pass


def get_db():
    """
    Generador de sesiones de base de datos.
    Se usa como dependencia en los endpoints de FastAPI.
    Garantiza que la sesión se cierra aunque ocurra un error.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()