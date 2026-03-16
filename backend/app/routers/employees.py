"""
Router de empleados.
Define los endpoints HTTP del módulo de empleados.
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.employee import EmployeeCreate, EmployeeUpdate, EmployeeResponse
import app.services.employee_service as employee_service

router = APIRouter(
    prefix="/employees",
    tags=["Empleados"]
)


@router.get("/", response_model=list[EmployeeResponse])
def list_employees(
    skip:  int = Query(default=0,   ge=0,  description="Registros a saltar"),
    limit: int = Query(default=100, ge=1, le=500, description="Límite de resultados"),
    db: Session = Depends(get_db)
):
    """Devuelve la lista de todos los empleados activos."""
    return employee_service.get_all_employees(db, skip=skip, limit=limit)


@router.get("/available", response_model=list[EmployeeResponse])
def list_available_employees(db: Session = Depends(get_db)):
    """Devuelve los empleados disponibles para asignar tareas."""
    return employee_service.get_available_employees(db)


@router.get("/{employee_id}", response_model=EmployeeResponse)
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    """Devuelve un empleado específico por su ID."""
    return employee_service.get_employee_by_id(db, employee_id)


@router.post("/", response_model=EmployeeResponse, status_code=201)
def create_employee(employee_data: EmployeeCreate, db: Session = Depends(get_db)):
    """Crea un nuevo empleado."""
    return employee_service.create_employee(db, employee_data)


@router.put("/{employee_id}", response_model=EmployeeResponse)
def update_employee(employee_id: int, employee_data: EmployeeUpdate, db: Session = Depends(get_db)):
    """Actualiza los datos de un empleado existente."""
    return employee_service.update_employee(db, employee_id, employee_data)


@router.delete("/{employee_id}")
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    """Desactiva un empleado (borrado lógico)."""
    return employee_service.delete_employee(db, employee_id)