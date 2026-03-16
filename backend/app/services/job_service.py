"""
Servicio de trabajos y checklists.
Contiene toda la lógica de negocio del módulo de trabajos.
"""
from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, status
from app.models.job import Job, ChecklistItem
from app.models.task import Task
from app.schemas.job import JobCreate, JobUpdate, ChecklistItemCreate, ChecklistItemUpdate


def _get_job_with_relations(db: Session, job_id: int) -> Job:
    """
    Obtiene un trabajo cargando todas sus relaciones.

    Args:
        db: Sesión de base de datos
        job_id: ID del trabajo

    Returns:
        Trabajo con relaciones cargadas

    Raises:
        HTTPException 404: Si el trabajo no existe
    """
    job = (
        db.query(Job)
        .options(joinedload(Job.checklist_items))
        .filter(Job.id == job_id, Job.is_active == True)
        .first()
    )
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Trabajo con ID {job_id} no encontrado"
        )
    return job


def get_all_jobs(db: Session, skip: int = 0, limit: int = 100) -> list[Job]:
    """Obtiene todos los trabajos activos con paginación."""
    return (
        db.query(Job)
        .options(joinedload(Job.checklist_items))
        .filter(Job.is_active == True)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_jobs_by_task(db: Session, task_id: int) -> list[Job]:
    """
    Obtiene todos los trabajos asociados a una tarea.

    Args:
        db: Sesión de base de datos
        task_id: ID de la tarea

    Returns:
        Lista de trabajos de esa tarea
    """
    return (
        db.query(Job)
        .options(joinedload(Job.checklist_items))
        .filter(Job.task_id == task_id, Job.is_active == True)
        .all()
    )


def get_job_by_id(db: Session, job_id: int) -> Job:
    """Obtiene un trabajo por su ID."""
    return _get_job_with_relations(db, job_id)


def create_job(db: Session, job_data: JobCreate) -> Job:
    """
    Crea un nuevo trabajo y sus ítems de checklist.
    Valida que la tarea origen exista.

    Args:
        db: Sesión de base de datos
        job_data: Datos del trabajo y checklist inicial

    Returns:
        Trabajo recién creado con sus ítems
    """
    # Valida que la tarea existe
    task = db.query(Task).filter(Task.id == job_data.task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarea con ID {job_data.task_id} no encontrada"
        )

    # Crea el trabajo
    checklist_data = job_data.checklist_items
    job_dict       = job_data.model_dump(exclude={"checklist_items"})
    db_job         = Job(**job_dict)
    db.add(db_job)
    db.flush()  # Obtiene el ID sin hacer commit todavía

    # Crea los ítems del checklist
    for item_data in checklist_data:
        db_item = ChecklistItem(job_id=db_job.id, **item_data.model_dump())
        db.add(db_item)

    db.commit()
    return _get_job_with_relations(db, db_job.id)


def update_job(db: Session, job_id: int, job_data: JobUpdate) -> Job:
    """
    Actualiza un trabajo existente.
    Solo modifica los campos enviados.
    """
    job         = _get_job_with_relations(db, job_id)
    update_data = job_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(job, field, value)

    db.commit()
    return _get_job_with_relations(db, job_id)


def delete_job(db: Session, job_id: int) -> dict:
    """Desactiva un trabajo (borrado lógico)."""
    job           = _get_job_with_relations(db, job_id)
    job.is_active = False
    db.commit()
    return {"message": f"Trabajo ID {job_id} desactivado correctamente"}


# ── Checklist Items ────────────────────────────────────────────

def add_checklist_item(db: Session, job_id: int, item_data: ChecklistItemCreate) -> Job:
    """
    Añade un ítem al checklist de un trabajo existente.

    Args:
        db: Sesión de base de datos
        job_id: ID del trabajo
        item_data: Datos del nuevo ítem

    Returns:
        Trabajo actualizado con el nuevo ítem
    """
    _get_job_with_relations(db, job_id)  # Valida que el trabajo existe
    db_item = ChecklistItem(job_id=job_id, **item_data.model_dump())
    db.add(db_item)
    db.commit()
    return _get_job_with_relations(db, job_id)


def update_checklist_item(db: Session, item_id: int, item_data: ChecklistItemUpdate) -> ChecklistItem:
    """
    Actualiza un ítem del checklist.
    Se usa para marcar ítems como completados o registrar incidencias.

    Args:
        db: Sesión de base de datos
        item_id: ID del ítem
        item_data: Campos a actualizar

    Returns:
        Ítem actualizado
    """
    item = db.query(ChecklistItem).filter(ChecklistItem.id == item_id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ítem de checklist con ID {item_id} no encontrado"
        )

    update_data = item_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(item, field, value)

    db.commit()
    db.refresh(item)
    return item