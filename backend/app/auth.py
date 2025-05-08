from app.database import SessionLocal
from app.models import User, Role, Employee, User
from app.schemas import UserCreate, UserOut, Token, EmployeeCreate
from app.security import hash_password, authenticate_user, create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from app.dependencies import get_current_user
from fastapi import APIRouter, HTTPException, Depends
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from . import models, schemas, database
from jose import JWTError, jwt
from datetime import datetime, timedelta

from .algorithms import assign_employees
from .schemas import EmployeeScheduleSchema, RequestOut
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
    new_user = models.User(username=user.username, hashed_password=hashed_password, role_id=1)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "Регистрация прошла успешно"}

@router.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter_by(username=user.username).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")

    token = create_access_token({"sub": db_user.username})
    return {"access_token": token, "token_type": "bearer","user_id": db_user.id,
        "is_admin": db_user.role_id==1, "name": db_user.username}

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


@router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(SessionLocal)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}

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
def get_requests(db: Session = Depends(get_db)):
    requests = db.query(models.Request).options(joinedload(models.Request.assigned_employees)).all()
    return requests


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

@router.get("/stations")
def get_stations(db: Session = Depends(get_db)):
    return db.query(models.Station).all()


@router.get("/disruptions", response_model=List[schemas.DisruptionOut])
def get_disruptions(db: Session = Depends(get_db)):
    disruptions = db.query(models.Disruption).options(joinedload(models.Disruption.station)).all()
    return disruptions
