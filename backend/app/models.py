import enum
from datetime import datetime
import pymysql
pymysql.install_as_MySQLdb()
from sqlalchemy import (
    create_engine, Column, Integer, String, Boolean, DateTime, Time,
    ForeignKey, Enum, Text, JSON, Table
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

# Настройка подключения к базе данных
SQLALCHEMY_DATABASE_URL = "mysql://assistant_user:meowing@mysql:3306/assistantsheduler"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Связующая таблица многие-ко-многим для заявок и сотрудников
request_employees = Table(
    'request_employees',
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
    role_id = Column(Integer, ForeignKey("roles.id"))
    employee_id = Column(Integer, ForeignKey("employees.id"))

    role = relationship("Role", back_populates="users")
    requests = relationship("Request", back_populates="user")
    employee = relationship(
        "Employee",
        back_populates="user",
        uselist=False,
        foreign_keys=[employee_id]
    )


class Request(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True, index=True)
    passenger_type = Column(String(50), nullable=False)

    departure_station_id = Column(Integer, ForeignKey("stations.id"), nullable=False)
    arrival_station_id = Column(Integer, ForeignKey("stations.id"), nullable=False)

    departure_station = relationship("Station", foreign_keys=[departure_station_id])
    arrival_station = relationship("Station", foreign_keys=[arrival_station_id])

    departure_time = Column(DateTime, nullable=False)
    status = Column(String(50), default="pending")
    luggage = Column(Boolean, default=False)

    assigned_employees = relationship('Employee', secondary='request_employees', back_populates="requests")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    user = relationship("User", back_populates="requests")

class Employee(Base):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    contact_info = Column(String(255), nullable=True)
    shift_start = Column(Time, nullable=False)
    shift_end = Column(Time, nullable=False)
    skills = Column(JSON, nullable=True)  # Список навыков сотрудников
    is_available = Column(Boolean, default=True)
    available_days = Column(JSON, nullable=True)  # ["mon", "tue", "wed"]
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    user = relationship(
        "User",
        back_populates="employee",
        foreign_keys="[User.employee_id]"
    )

    requests = relationship('Request', secondary='request_employees', back_populates="assigned_employees")
    schedules = relationship("Schedule", backref="employee", cascade="all, delete-orphan")

class DisruptionTypeEnum(str, enum.Enum):
    delay = 'delay'
    no_show = 'no_show'
    cancel = 'cancel'
    reschedule = 'reschedule'

class Station(Base):
    __tablename__ = "stations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)

    disruptions = relationship("Disruption", back_populates="station", cascade="all, delete-orphan")

class Disruption(Base):
    __tablename__ = "disruptions"

    id = Column(Integer, primary_key=True, index=True)
    station_id = Column(Integer, ForeignKey("stations.id", ondelete="CASCADE"), nullable=False)
    type = Column(Enum(DisruptionTypeEnum), nullable=False)
    description = Column(Text)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    station = relationship("Station", back_populates="disruptions")

class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id", ondelete="CASCADE"), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    is_available = Column(Boolean, default=True)

class EmergencyCall(Base):
    __tablename__ = "emergency_calls"

    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(Integer, ForeignKey("requests.id"))
    message = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

class ReassignmentRequest(Base):
    __tablename__ = "reassignment_requests"

    id = Column(Integer, primary_key=True)
    request_id = Column(Integer, ForeignKey("requests.id"))
    reason = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)

# Создание таблиц в базе данных
Base.metadata.create_all(bind=engine)