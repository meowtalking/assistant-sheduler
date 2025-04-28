from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

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
DATABASE_URL = "mysql+mysqlconnector://username:password@localhost/db_name"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)
