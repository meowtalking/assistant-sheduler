import pymysql
pymysql.install_as_MySQLdb()
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from app.database import Base
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "mysql://assistant_user:meowing@mysql:3306/assistantsheduler"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

from sqlalchemy.orm import relationship

from sqlalchemy import Table

request_employee = Table(
    'request_employee',
    Base.metadata,
    Column('request_id', Integer, ForeignKey('requests.id')),
    Column('employee_id', Integer, ForeignKey('employees.id'))
)
class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    users = relationship("User", back_populates="role")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role_id = Column(Integer, ForeignKey("roles.id"))  # <- Обязательный внешний ключ!

    role = relationship("Role", back_populates="users")
    requests = relationship("Request", back_populates="user")
class Request(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True, index=True)
    passenger_type = Column(String(50), nullable=True)
    departure_station = Column(String(100), nullable=False)
    arrival_station = Column(String(100), nullable=False)
    departure_time = Column(DateTime, nullable=False)
    status = Column(String(50), default="pending")
    luggage = Column(Boolean, nullable=True)
    assigned_employee_ids = Column(String(255), nullable=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    user = relationship("User", back_populates="requests")
    employees = relationship("Employee", secondary=request_employee, back_populates="requests")

class Employee(Base):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    contact_info = Column(String(255), nullable=True)
    shift_time = Column(String(50), nullable=False)
    skills = Column(String(255), nullable=True)  # Список навыков сотрудников
    is_available = Column(Boolean, default=True)
    requests = relationship("Request", secondary=request_employee, back_populates="employees")

# Подключение к базе данных
#DATABASE_URL = "mysql://root:meowmeow@localhost/assistantsheduler"

Base.metadata.create_all(bind=engine)


