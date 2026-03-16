"""
Router de tareas.
Define los endpoints HTTP del módulo de tareas y agenda.
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import date
from app.core.database import get_db
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse, TaskDetailResponse
import app.services.task_service as task_service

router = APIRouter(
    prefix="/tasks",
    tags=["Tareas & Agenda"]
)


@router.get("/", response_model=list[TaskResponse])
def list_tasks(
    skip:  int = Query(default=0,   ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """Devuelve todas las tareas activas."""
    return task_service.get_all_tasks(db, skip=skip, limit=limit)


@router.get("/agenda/day", response_model=list[TaskDetailResponse])
def get_agenda_by_day(
    date: date = Query(..., description="Fecha a consultar (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """Devuelve todas las tareas de un día concreto."""
    return task_service.get_tasks_by_date(db, date)


@router.get("/agenda/week", response_model=list[TaskDetailResponse])
def get_agenda_by_week(
    start_date: date = Query(..., description="Fecha de inicio (YYYY-MM-DD)"),
    end_date:   date = Query(..., description="Fecha de fin (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """Devuelve todas las tareas entre dos fechas."""
    return task_service.get_tasks_by_week(db, start_date, end_date)


@router.get("/{task_id}", response_model=TaskDetailResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    """Devuelve una tarea específica con todos sus detalles."""
    return task_service.get_task_by_id(db, task_id)


@router.post("/", response_model=TaskDetailResponse, status_code=201)
def create_task(task_data: TaskCreate, db: Session = Depends(get_db)):
    """Crea una nueva tarea y asigna empleados."""
    return task_service.create_task(db, task_data)


@router.put("/{task_id}", response_model=TaskDetailResponse)
def update_task(task_id: int, task_data: TaskUpdate, db: Session = Depends(get_db)):
    """Actualiza una tarea existente."""
    return task_service.update_task(db, task_id, task_data)


@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """Desactiva una tarea (borrado lógico)."""
    return task_service.delete_task(db, task_id)