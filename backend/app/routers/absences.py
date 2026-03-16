"""
Router de ausencias.
Define los endpoints HTTP del módulo de ausencias de personal.
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import date
from app.core.database import get_db
from app.schemas.absence import AbsenceCreate, AbsenceUpdate, AbsenceDetailResponse
import app.services.absence_service as absence_service

router = APIRouter(
    prefix="/absences",
    tags=["Ausencias"]
)


@router.get("/", response_model=list[AbsenceDetailResponse])
def list_absences(
    skip:  int = Query(default=0,   ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """Devuelve todas las ausencias activas."""
    return absence_service.get_all_absences(db, skip=skip, limit=limit)


@router.get("/by-employee/{employee_id}", response_model=list[AbsenceDetailResponse])
def get_absences_by_employee(employee_id: int, db: Session = Depends(get_db)):
    """Devuelve todas las ausencias de un empleado concreto."""
    return absence_service.get_absences_by_employee(db, employee_id)


@router.get("/by-date-range", response_model=list[AbsenceDetailResponse])
def get_absences_by_date_range(
    start: date = Query(..., description="Fecha de inicio (YYYY-MM-DD)"),
    end:   date = Query(..., description="Fecha de fin (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """Devuelve ausencias que se solapan con un rango de fechas."""
    return absence_service.get_absences_by_date_range(db, start, end)


@router.get("/check-availability/{employee_id}")
def check_employee_availability(
    employee_id: int,
    date: date = Query(..., description="Fecha a comprobar (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """Comprueba si un empleado está disponible en una fecha concreta."""
    available = absence_service.is_employee_available(db, employee_id, date)
    return {
        "employee_id": employee_id,
        "date":        str(date),
        "available":   available
    }


@router.get("/{absence_id}", response_model=AbsenceDetailResponse)
def get_absence(absence_id: int, db: Session = Depends(get_db)):
    """Devuelve una ausencia específica."""
    return absence_service.get_absences_by_employee(db, absence_id)


@router.post("/", response_model=AbsenceDetailResponse, status_code=201)
def create_absence(absence_data: AbsenceCreate, db: Session = Depends(get_db)):
    """Registra una nueva ausencia de personal."""
    return absence_service.create_absence(db, absence_data)


@router.put("/{absence_id}", response_model=AbsenceDetailResponse)
def update_absence(absence_id: int, absence_data: AbsenceUpdate, db: Session = Depends(get_db)):
    """Actualiza una ausencia existente. Úsalo también para aprobarla."""
    return absence_service.update_absence(db, absence_id, absence_data)


@router.delete("/{absence_id}")
def delete_absence(absence_id: int, db: Session = Depends(get_db)):
    """Elimina una ausencia (borrado lógico)."""
    return absence_service.delete_absence(db, absence_id)