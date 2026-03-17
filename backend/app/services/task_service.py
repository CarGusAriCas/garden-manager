"""
Servicio de tareas.
Contiene toda la lógica de negocio del módulo de tareas.
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import date
from app.models.task import Task
from app.models.employee import Employee
from app.schemas.task import TaskCreate, TaskUpdate


def _get_employees_by_ids(db: Session, employee_ids: list[int]) -> list[Employee]:
    """
    Obtiene una lista de empleados por sus IDs.
    Valida que todos los IDs existan.

    Args:
        db: Sesión de base de datos
        employee_ids: Lista de IDs de empleados

    Returns:
        Lista de objetos Employee

    Raises:
        HTTPException 404: Si algún ID no existe
    """
    employees = db.query(Employee).filter(Employee.id.in_(employee_ids)).all()
    if len(employees) != len(employee_ids):
        found_ids    = {e.id for e in employees}
        missing_ids  = set(employee_ids) - found_ids
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Empleados no encontrados: {missing_ids}"
        )
    return employees


def get_all_tasks(db: Session, skip: int = 0, limit: int = 100) -> list[Task]:
    """Obtiene todas las tareas activas cargando relaciones en una sola consulta."""
    from sqlalchemy.orm import joinedload
    return (
        db.query(Task)
        .options(
            joinedload(Task.client),
            joinedload(Task.employees)
        )
        .filter(Task.is_active == True)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_tasks_by_week(db: Session, start_date: date, end_date: date) -> list[Task]:
    """Obtiene tareas de una semana cargando relaciones en una sola consulta."""
    from sqlalchemy.orm import joinedload
    return (
        db.query(Task)
        .options(
            joinedload(Task.client),
            joinedload(Task.employees)
        )
        .filter(
            Task.date >= start_date,
            Task.date <= end_date,
            Task.is_active == True
        )
        .order_by(Task.date, Task.start_time)
        .all()
    )


def get_tasks_by_date(db: Session, target_date: date) -> list[Task]:
    """Obtiene tareas de un día cargando relaciones en una sola consulta."""
    from sqlalchemy.orm import joinedload
    return (
        db.query(Task)
        .options(
            joinedload(Task.client),
            joinedload(Task.employees)
        )
        .filter(Task.date == target_date, Task.is_active == True)
        .all()
    )


def get_task_by_id(db: Session, task_id: int) -> Task:
    """
    Obtiene una tarea por su ID.

    Raises:
        HTTPException 404: Si la tarea no existe
    """
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarea con ID {task_id} no encontrada"
        )
    return task


def create_task(db: Session, task_data: TaskCreate) -> Task:
    """
    Crea una nueva tarea y asigna empleados.

    Args:
        db: Sesión de base de datos
        task_data: Datos validados de la nueva tarea

    Returns:
        Tarea recién creada con empleados asignados
    """
    # Extrae los IDs de empleados antes de crear el objeto
    employee_ids = task_data.employee_ids
    task_dict    = task_data.model_dump(exclude={"employee_ids"})

    db_task = Task(**task_dict)

    # Asigna empleados si se proporcionaron
    if employee_ids:
        employees = _get_employees_by_ids(db, employee_ids)
        db_task.employees = employees

    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    # Recarga el objeto completo con todas sus relaciones
    return get_task_by_id(db, db_task.id)

def update_task(db: Session, task_id: int, task_data: TaskUpdate) -> Task:
    """
    Actualiza una tarea existente.
    Si se envían employee_ids, reemplaza la asignación completa.
    """
    task        = get_task_by_id(db, task_id)
    update_data = task_data.model_dump(exclude_unset=True)

    # Maneja la actualización de empleados por separado
    employee_ids = update_data.pop("employee_ids", None)
    if employee_ids is not None:
        task.employees = _get_employees_by_ids(db, employee_ids)

    for field, value in update_data.items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)
    return get_task_by_id(db, task.id)


def delete_task(db: Session, task_id: int) -> dict:
    """Desactiva una tarea (borrado lógico)."""
    task          = get_task_by_id(db, task_id)
    task.is_active = False
    db.commit()
    return {"message": f"Tarea '{task.title}' desactivada correctamente"}