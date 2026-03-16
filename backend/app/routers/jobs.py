"""
Router de trabajos y checklists.
Define los endpoints HTTP del módulo de trabajos.
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.job import (
    JobCreate, JobUpdate, JobResponse,
    ChecklistItemCreate, ChecklistItemUpdate, ChecklistItemResponse
)
import app.services.job_service as job_service

router = APIRouter(
    prefix="/jobs",
    tags=["Trabajos & Checklists"]
)


@router.get("/", response_model=list[JobResponse])
def list_jobs(
    skip:  int = Query(default=0,   ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """Devuelve todos los trabajos activos."""
    return job_service.get_all_jobs(db, skip=skip, limit=limit)


@router.get("/by-task/{task_id}", response_model=list[JobResponse])
def get_jobs_by_task(task_id: int, db: Session = Depends(get_db)):
    """Devuelve todos los trabajos asociados a una tarea."""
    return job_service.get_jobs_by_task(db, task_id)


@router.get("/{job_id}", response_model=JobResponse)
def get_job(job_id: int, db: Session = Depends(get_db)):
    """Devuelve un trabajo específico con su checklist completo."""
    return job_service.get_job_by_id(db, job_id)


@router.post("/", response_model=JobResponse, status_code=201)
def create_job(job_data: JobCreate, db: Session = Depends(get_db)):
    """Crea un nuevo trabajo con su checklist inicial."""
    return job_service.create_job(db, job_data)


@router.put("/{job_id}", response_model=JobResponse)
def update_job(job_id: int, job_data: JobUpdate, db: Session = Depends(get_db)):
    """Actualiza un trabajo existente."""
    return job_service.update_job(db, job_id, job_data)


@router.delete("/{job_id}")
def delete_job(job_id: int, db: Session = Depends(get_db)):
    """Desactiva un trabajo (borrado lógico)."""
    return job_service.delete_job(db, job_id)


# ── Checklist ──────────────────────────────────────────────────

@router.post("/{job_id}/checklist", response_model=JobResponse)
def add_checklist_item(
    job_id: int,
    item_data: ChecklistItemCreate,
    db: Session = Depends(get_db)
):
    """Añade un ítem al checklist de un trabajo."""
    return job_service.add_checklist_item(db, job_id, item_data)


@router.patch("/checklist/{item_id}", response_model=ChecklistItemResponse)
def update_checklist_item(
    item_id: int,
    item_data: ChecklistItemUpdate,
    db: Session = Depends(get_db)
):
    """Actualiza un ítem del checklist. Úsalo para marcar completado o registrar incidencias."""
    return job_service.update_checklist_item(db, item_id, item_data)