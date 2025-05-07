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

    new_employee = Employee(
        name=employee.name,
        contact_info=employee.contact_info,
        shift_time=employee.shift_time,
        skills=employee.skills,
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
    # Получаем сотрудников, чьи смены не пересекаются с временем заявки
    employees = db.query(models.Employee).filter(
        models.Employee.shift_start <= departure_time,
        models.Employee.shift_end >= departure_time
    ).all()
    return employees

@router.post("/request")
def create_request(request: schemas.RequestCreate, db: Session = Depends(get_db)):
    # Проверка на наличие доступных сотрудников
    print(request)
    available_employees = get_available_employees(request.departure_time, db)
    if not available_employees:
        raise HTTPException(status_code=400, detail="Нет доступных сотрудников на указанное время")

    # Создаем заявку
    db_request = models.Request(**request.dict())

    # Назначаем первого доступного сотрудника на заявку
    db_request.assigned_employee_ids = [available_employees[0].id]

    db.add(db_request)
    db.commit()
    db.refresh(db_request)

    return {"message": "Заявка создана", "assigned_employee_id": available_employees[0].id}


@router.get("/requests", response_model=List[RequestOut])
def get_requests(db: Session = Depends(get_db)):
    return db.query(models.Request).all()

@router.get("/api/schedule", response_model=List[EmployeeScheduleSchema])
def get_schedule(db: Session = Depends(get_db)):
    # Например, фильтрация по is_available = True
    return db.query(Employee).filter(Employee.is_available == True).all()

@router.get("/stations")
def get_stations(db: Session = Depends(get_db)):
    return db.query(models.Station).all()


@router.get("/disruptions", response_model=List[schemas.DisruptionOut])
def get_disruptions(db: Session = Depends(get_db)):
    disruptions = db.query(models.Disruption).options(joinedload(models.Disruption.station)).all()
    return disruptions
