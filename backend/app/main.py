"""
Punto de entrada principal de la aplicación GardenManager.
Aquí se inicializa FastAPI y se registran todos los routers.
"""
from fastapi import FastAPI
from app.core.config import settings
from app.core.database import Base, engine
from app.routers import clients
from app.routers import employees
from app.routers import tasks
from app.routers import jobs
from app.routers import absences

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="API de gestión para empresa de jardinería",
)

app.include_router(clients.router)
app.include_router(employees.router)
app.include_router(tasks.router)
app.include_router(jobs.router)
app.include_router(absences.router)

@app.get("/")
def root():
    """Endpoint de bienvenida para verificar que el servidor funciona."""
    return {
        "app": settings.app_name,
        "version": settings.app_version,
        "status": "funcionando",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    """Endpoint de verificación del estado del servidor."""
    return {"status": "ok"}