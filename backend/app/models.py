import pymysql
pymysql.install_as_MySQLdb()
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "mysql://root:meowmeow@mysql:3306/assistantsheduler"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)

    users = relationship("User", back_populates="role")

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role_id = Column(Integer, ForeignKey('roles.id'), nullable=False)

    role = relationship("Role", back_populates="users")

class Employee(Base):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    contact_info = Column(String(255), nullable=True)
    shift_time = Column(String(50), nullable=False)
    skills = Column(String(255), nullable=True)  # Список навыков сотрудников

class Request(Base):
    __tablename__ = 'requests'

    id = Column(Integer, primary_key=True, autoincrement=True)
    passenger_type = Column(String(50))  # 'слабовидящий', 'колясочник'
    departure_station = Column(String(100), nullable=False)
    arrival_station = Column(String(100), nullable=False)
    departure_time = Column(DateTime, nullable=False)
    status = Column(String(50), default='Ожидает')  # Статус заявки
    luggage = Column(Boolean, default=False)  # Нужен ли дополнительный сотрудник для багажа
    assigned_employee_ids = Column(String(255))  # Список ID сотрудников

# Подключение к базе данных
#DATABASE_URL = "mysql://root:meowmeow@localhost/assistantsheduler"

Base.metadata.create_all(bind=engine)
from fastapi import FastAPI
from pydantic import BaseModel



class Employee(BaseModel):
    id: int
    name: str
    shift_time: str

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from app.database import Base

class Request(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True, index=True)
    departure_station = Column(String(100), nullable=False)
    arrival_station = Column(String(100), nullable=False)
    departure_time = Column(DateTime, nullable=False)
    passenger_type = Column(String(50))
    status = Column(String(50))
    luggage = Column(Boolean)
    assigned_employee_ids = Column(String(255))
