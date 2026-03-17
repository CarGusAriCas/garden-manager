"""
Servicio de empleados.
Contiene toda la lógica de negocio del módulo de empleados.
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate, EmployeeUpdate


def get_all_employees(db: Session, skip: int = 0, limit: int = 100) -> list[Employee]:
    """
    Obtiene todos los empleados activos con paginación.

    Args:
        db: Sesión de base de datos
        skip: Número de registros a saltar
        limit: Número máximo de registros a devolver

    Returns:
        Lista de empleados activos
    """
    return (
        db.query(Employee)
        .filter(Employee.is_active == True)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_employee_by_id(db: Session, employee_id: int) -> Employee:
    """
    Obtiene un empleado por su ID.

    Args:
        db: Sesión de base de datos
        employee_id: ID del empleado a buscar

    Returns:
        Empleado encontrado

    Raises:
        HTTPException 404: Si el empleado no existe
    """
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Empleado con ID {employee_id} no encontrado"
        )
    return employee


def create_employee(db: Session, employee_data: EmployeeCreate) -> Employee:
    """
    Crea un nuevo empleado en la base de datos.

    Args:
        db: Sesión de base de datos
        employee_data: Datos validados del nuevo empleado

    Returns:
        Empleado recién creado

    Raises:
        HTTPException 400: Si el email ya está registrado
    """
    if employee_data.email:
        existing = db.query(Employee).filter(Employee.email == employee_data.email).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El email {employee_data.email} ya está registrado"
            )

    db_employee = Employee(**employee_data.model_dump())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee


def update_employee(db: Session, employee_id: int, employee_data: EmployeeUpdate) -> Employee:
    """
    Actualiza los datos de un empleado existente.
    Solo modifica los campos que se envían en la petición.

    Args:
        db: Sesión de base de datos
        employee_id: ID del empleado a actualizar
        employee_data: Campos a actualizar

    Returns:
        Empleado actualizado
    """
    employee = get_employee_by_id(db, employee_id)

    update_data = employee_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(employee, field, value)

    db.commit()
    db.refresh(employee)
    return employee


def delete_employee(db: Session, employee_id: int) -> dict:
    """
    Desactiva un empleado (borrado lógico).
    No se elimina de la BD — se marca como inactivo para conservar el historial.

    Args:
        db: Sesión de base de datos
        employee_id: ID del empleado a desactivar

    Returns:
        Mensaje de confirmación
    """
    employee = get_employee_by_id(db, employee_id)
    employee.is_active = False
    db.commit()
    return {"message": f"Empleado {employee.name} desactivado correctamente"}


def get_available_employees(db: Session) -> list[Employee]:
    """
    Obtiene todos los empleados activos disponibles.
    En fases posteriores este filtro incluirá ausencias y tareas asignadas.

    Args:
        db: Sesión de base de datos

    Returns:
        Lista de empleados disponibles
    """
    return db.query(Employee).filter(Employee.is_active == True).all()


def update_employee_coordinates(db: Session, employee_id: int, lat: float, lon: float) -> Employee:
    """
    Actualiza las coordenadas geográficas de un empleado.

    Args:
        db: Sesión de base de datos
        employee_id: ID del empleado
        lat: Latitud
        lon: Longitud

    Returns:
        Empleado actualizado
    """
    employee           = get_employee_by_id(db, employee_id)
    employee.latitude  = lat
    employee.longitude = lon
    db.commit()
    db.refresh(employee)
    return employee