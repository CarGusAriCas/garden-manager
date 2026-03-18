"""
Punto de entrada principal de la aplicación GardenManager.
Aquí se inicializa FastAPI y se registran todos los routers.
Las migraciones de BD las gestiona Alembic — no usar create_all aquí.
"""
from fastapi import FastAPI
from app.core.config import settings
from app.routers import clients, employees, tasks, jobs, absences, notifications, auth


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
app.include_router(notifications.router)
app.include_router(auth.router)


@app.get("/")
def root():
    """Endpoint de bienvenida para verificar que el servidor funciona."""
    return {
        "app":     settings.app_name,
        "version": settings.app_version,
        "status":  "funcionando",
        "docs":    "/docs"
    }


@app.get("/health")
def health_check():
    """Endpoint de verificación del estado del servidor."""
    return {"status": "ok"}


@app.get("/ping")
def ping():
    """Endpoint de keep-alive para evitar el spin-down de Render."""
    return {"pong": True}