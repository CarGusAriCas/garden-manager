"""
Servicio de ausencias.
Contiene toda la lógica de negocio del módulo de ausencias.
"""
from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, status
from datetime import date
from app.models.absence import Absence
from app.models.employee import Employee
from app.schemas.absence import AbsenceCreate, AbsenceUpdate


def _get_absence_with_relations(db: Session, absence_id: int) -> Absence:
    """
    Obtiene una ausencia cargando sus relaciones.

    Raises:
        HTTPException 404: Si la ausencia no existe
    """
    absence = (
        db.query(Absence)
        .options(joinedload(Absence.employee))
        .filter(Absence.id == absence_id, Absence.is_active == True)
        .first()
    )
    if not absence:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ausencia con ID {absence_id} no encontrada"
        )
    return absence


def get_all_absences(db: Session, skip: int = 0, limit: int = 100) -> list[Absence]:
    """Obtiene todas las ausencias activas con paginación."""
    return (
        db.query(Absence)
        .options(joinedload(Absence.employee))
        .filter(Absence.is_active == True)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_absences_by_employee(db: Session, employee_id: int) -> list[Absence]:
    """
    Obtiene todas las ausencias de un empleado concreto.

    Args:
        db: Sesión de base de datos
        employee_id: ID del empleado

    Returns:
        Lista de ausencias del empleado
    """
    return (
        db.query(Absence)
        .options(joinedload(Absence.employee))
        .filter(Absence.employee_id == employee_id, Absence.is_active == True)
        .all()
    )


def get_absences_by_date_range(db: Session, start: date, end: date) -> list[Absence]:
    """
    Obtiene ausencias que se solapan con un rango de fechas.
    Útil para saber quién está disponible en una semana concreta.

    Args:
        db: Sesión de base de datos
        start: Fecha de inicio del rango
        end: Fecha de fin del rango

    Returns:
        Lista de ausencias que coinciden con el rango
    """
    return (
        db.query(Absence)
        .options(joinedload(Absence.employee))
        .filter(
            Absence.is_active == True,
            Absence.start_date <= end,
            Absence.end_date   >= start,
        )
        .all()
    )


def is_employee_available(db: Session, employee_id: int, target_date: date) -> bool:
    """
    Comprueba si un empleado está disponible en una fecha concreta.
    Devuelve False si tiene una ausencia aprobada que cubre esa fecha.

    Args:
        db: Sesión de base de datos
        employee_id: ID del empleado
        target_date: Fecha a comprobar

    Returns:
        True si está disponible, False si está ausente
    """
    absence = (
        db.query(Absence)
        .filter(
            Absence.employee_id == employee_id,
            Absence.is_active   == True,
            Absence.is_approved == True,
            Absence.start_date  <= target_date,
            Absence.end_date    >= target_date,
        )
        .first()
    )
    return absence is None


def create_absence(db: Session, absence_data: AbsenceCreate) -> Absence:
    """
    Crea una nueva ausencia.
    Valida que el empleado exista y que no tenga otra ausencia solapada.

    Args:
        db: Sesión de base de datos
        absence_data: Datos de la ausencia

    Returns:
        Ausencia recién creada

    Raises:
        HTTPException 404: Si el empleado no existe
        HTTPException 400: Si hay solapamiento con otra ausencia
    """
    # Valida que el empleado existe
    employee = db.query(Employee).filter(Employee.id == absence_data.employee_id).first()
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Empleado con ID {absence_data.employee_id} no encontrado"
        )

    # Valida que no hay solapamiento con otra ausencia del mismo empleado
    overlap = (
        db.query(Absence)
        .filter(
            Absence.employee_id == absence_data.employee_id,
            Absence.is_active   == True,
            Absence.start_date  <= absence_data.end_date,
            Absence.end_date    >= absence_data.start_date,
        )
        .first()
    )
    if overlap:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El empleado ya tiene una ausencia registrada entre "
                   f"{overlap.start_date} y {overlap.end_date}"
        )

    db_absence = Absence(**absence_data.model_dump())
    db.add(db_absence)
    db.commit()
    return _get_absence_with_relations(db, db_absence.id)


def update_absence(db: Session, absence_id: int, absence_data: AbsenceUpdate) -> Absence:
    """Actualiza una ausencia existente."""
    absence     = _get_absence_with_relations(db, absence_id)
    update_data = absence_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(absence, field, value)

    db.commit()
    return _get_absence_with_relations(db, absence_id)


def delete_absence(db: Session, absence_id: int) -> dict:
    """Desactiva una ausencia (borrado lógico)."""
    absence           = _get_absence_with_relations(db, absence_id)
    absence.is_active = False
    db.commit()
    return {"message": f"Ausencia ID {absence_id} eliminada correctamente"}