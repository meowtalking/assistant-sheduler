import pymysql
pymysql.install_as_MySQLdb()
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from .database import Base
from sqlalchemy.orm import relationship
from app.database import Base
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "mysql://assistant_user:meowing@mysql:3306/assistantsheduler"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    users = relationship("User", back_populates="role")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    is_disabled = Column(Boolean, default=False)
    role_id = Column(Integer, ForeignKey("roles.id"))  # <- Обязательный внешний ключ!

    role = relationship("Role", back_populates="users")
    requests = relationship("Request", back_populates="user")
class Request(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    departure_station = Column(String(100))
    arrival_station = Column(String(100))
    departure_time = Column(DateTime)
    status = Column(String(50), default="Ожидает")

    user = relationship("User", back_populates="requests")


class Employee(Base):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    contact_info = Column(String(255), nullable=True)
    shift_time = Column(String(50), nullable=False)
    skills = Column(String(255), nullable=True)  # Список навыков сотрудников

# Подключение к базе данных
#DATABASE_URL = "mysql://root:meowmeow@localhost/assistantsheduler"

Base.metadata.create_all(bind=engine)
from fastapi import FastAPI
from pydantic import BaseModel



class Employee(BaseModel):
    id: int
    name: str
    shift_time: str

