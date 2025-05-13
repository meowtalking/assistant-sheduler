from app.database import SessionLocal
from app.models import User, Role, Employee, User
from app.schemas import UserCreate, UserOut, Token, EmployeeCreate
from app.security import create_access_token
from app.dependencies import get_current_user
from fastapi import APIRouter, HTTPException, Depends
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from . import models, schemas, database
from datetime import datetime
from fastapi import Body
from .algorithms import assign_employees
from .models import Request
from .schemas import EmployeeScheduleSchema, EmergencyRequestIn, ReassignRequestSchema
from typing import List
from sqlalchemy.orm import joinedload
router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def get_password_hash(password):
    return pwd_context.hash(password)


@router.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter_by(username=user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Пользователь уже существует")

    hashed_password = get_password_hash(user.password)
    new_user = models.User(username=user.username, hashed_password=hashed_password, role_id=2)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "Регистрация прошла успешно"}

@router.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter_by(username=user.username).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")

    token = create_access_token({"sub": db_user.id})
    return {"access_token": token, "token_type": "bearer","user_id": db_user.id,
        "is_admin": db_user.role_id==1, "name": db_user.username, "role_id": db_user.role_id}

@router.post("/admin/employees")
def create_employee(
    employee: EmployeeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Проверка прав
    if not current_user.role.name == "admin":
        raise HTTPException(status_code=403, detail="Доступ только для администраторов")

    # Создание нового сотрудника
    new_employee = Employee(
        name=employee.name,
        contact_info=employee.contact_info,
        skills=employee.skills,
        shift_start=employee.shift_start,
        shift_end=employee.shift_end,
        available_days=employee.available_days,
    )

    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)

    return {"message": "Сотрудник успешно создан", "employee_id": new_employee.id}

# Функция для получения доступных сотрудников на указанное время
def get_available_employees(departure_time: datetime, db: Session) -> List[models.Employee]:
    employees = db.query(models.Employee).filter(
        models.Employee.shift_start <= departure_time,
        models.Employee.shift_end >= departure_time,
        models.Employee.is_available == True  # Проверяем, что сотрудник доступен
    ).all()
    return employees

@router.post("/request")
def create_request(request: schemas.RequestCreate, db: Session = Depends(get_db)):
    # Прежде чем назначить сотрудников, проверим доступных
    all_employees = get_available_employees(request.departure_time, db)

    if not all_employees:
        raise HTTPException(status_code=400, detail="Нет доступных сотрудников на указанное время")

    db_request = models.Request(**request.dict())
    assigned_requests = assign_employees([db_request], all_employees)

    if not assigned_requests or not assigned_requests[0].assigned_employees:
        raise HTTPException(status_code=400, detail="Не удалось назначить сотрудников")

    db_request.assigned_employees = assigned_requests[0].assigned_employees
    db.add(db_request)
    db.commit()
    db.refresh(db_request)

    return {
        "message": "Заявка создана",
        "assigned_employee_names": [e.name for e in db_request.assigned_employees]
    }

@router.get("/requests", response_model=List[schemas.RequestOut])
def get_upcoming_requests(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    now = datetime.utcnow()
    query = db.query(models.Request).options(joinedload(models.Request.assigned_employees))

    query = query.filter(
        models.Request.departure_time >= now,
        models.Request.status.notin_(["cancelled", "completed"])
    )

    # Если пользователь не администратор (роль не 1), фильтруем по user_id
    if current_user.role_id != 1:
        query = query.filter(models.Request.user_id == current_user.id)

    return query.all()

@router.get("/api/schedule", response_model=List[EmployeeScheduleSchema])
def get_schedule(db: Session = Depends(get_db)):
    # Получаем всех сотрудников с доступным временем
    employees = db.query(Employee).filter(Employee.is_available == True).all()

    # Преобразуем сотрудников в нужный формат для ответа
    schedule = []
    for employee in employees:
        schedule.append({
            "id": employee.id,
            "name": employee.name,
            "shift_time": f"{employee.shift_start} - {employee.shift_end}"  # Форматируем shift_time
        })
    return schedule

@router.get("/assistant/requests", response_model=List[schemas.RequestOut])
def get_assistant_requests(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        # Проверка роли
        if current_user.role.id != 3:
            raise HTTPException(status_code=403, detail="Доступ запрещён")

        # Находим сотрудника, связанного с текущим пользователем
        employee = db.query(Employee).filter(Employee.user_id == current_user.id).first()
        if not employee:
            raise HTTPException(status_code=404, detail="Сотрудник не найден")

        # Текущая дата и время
        current_time = datetime.utcnow()

        # Получаем заявки, где:
        # 1. Сотрудник назначен
        # 2. Дата заявки ещё не наступила
        requests = (
            db.query(Request)
            .join(Request.assigned_employees)
            .filter(
                Employee.id == employee.id,
                Request.departure_time > current_time  # Фильтр по дате
            )
            .options(joinedload(Request.assigned_employees))
            .order_by(Request.departure_time.asc())  # Сортировка по дате
            .all()
        )
        return requests
    except Exception as e:
        print(f"ERROR: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal error")

@router.get("/stations")
def get_stations(db: Session = Depends(get_db)):
    return db.query(models.Station).all()

@router.get("/disruptions", response_model=List[schemas.DisruptionOut])
def get_disruptions(db: Session = Depends(get_db)):
    disruptions = db.query(models.Disruption).options(joinedload(models.Disruption.station)).all()
    return disruptions

@router.get("/admin/requests", response_model=List[schemas.RequestOut])
def get_all_requests(db: Session = Depends(get_db)):
    return db.query(models.Request).all()

@router.post("/admin/reassign")
def reassign_request(
    data: ReassignRequestSchema,
    db: Session = Depends(get_db)
):
    request = db.query(models.Request).filter(models.Request.id == data.request_id).first()
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")

    employees = db.query(models.Employee).filter(models.Employee.id.in_(data.employee_ids)).all()
    if len(employees) != len(data.employee_ids):
        raise HTTPException(status_code=400, detail="One or more employees not found")

    request.assigned_employees = employees
    db.commit()
    return {"message": "Request reassigned successfully"}

@router.get("/analytics/stats")
def get_stats(db: Session = Depends(get_db)):
    total_requests = db.query(models.Request).count()
    completed_requests = db.query(models.Request).filter(models.Request.status == "completed").count()
    pending_requests = db.query(models.Request).filter(models.Request.status == "pending").count()

    return {
        "total_requests": total_requests,
        "completed_requests": completed_requests,
        "pending_requests": pending_requests
    }

@router.post("/emergency/report")
def request_help(data: EmergencyRequestIn, db: Session = Depends(get_db)):
    call = models.EmergencyCall(request_id=data.request_id, message=data.message)
    db.add(call)
    db.commit()
    return {"message": "Emergency logged"}

@router.get("/emergency/requests")
def get_emergency_calls(db: Session = Depends(get_db)):
    return db.query(models.EmergencyCall).all()

@router.put("/user/update-username")
def update_username(
    new_username: str = Body(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    current_user.username = new_username
    db.commit()
    db.refresh(current_user)
    return {"message": "Username updated"}

@router.get("/admin/employees", response_model=list[schemas.EmployeeOut])
def get_all_employees(db: Session = Depends(get_db)):
    return db.query(models.Employee).all()

@router.patch("/assistant/requests/{request_id}/status")
def update_request_status(
    request_id: int,
    data: dict = Body(...),
    db: Session = Depends(get_db)
):
    request = db.query(models.Request).filter(models.Request.id == request_id).first()
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")

    new_status = data.get("status")
    if not new_status:
        raise HTTPException(status_code=400, detail="Status is required")

    request.status = new_status
    db.commit()
    return {"message": "Status updated"}
