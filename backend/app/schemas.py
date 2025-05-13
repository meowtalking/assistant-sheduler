from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List
class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class EmployeeScheduleSchema(BaseModel):
    id: int
    name: str
    shift_time: str

    class Config:
        orm_mode = True

class EmployeeCreate(BaseModel):
    name: str
    contact_info: str
    skills: List[str]
    shift_start: str  # Например, '08:00:00'
    shift_end: str    # Например, '20:00:00'
    available_days: List[str]  # Например, ['mon', 'tue', 'wed', 'thu']

    class Config:
        orm_mode = True

class EmployeeOut(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class StationBase(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class RequestCreate(BaseModel):
    user_id: int
    passenger_type: Optional[str]
    departure_station_id: int  # Измените на id
    arrival_station_id: int  # Измените на id
    departure_time: datetime
    luggage: Optional[bool] = False

class RequestOut(BaseModel):
    id: int
    status: str
    departure_station: StationBase
    arrival_station: StationBase
    passenger_type: str
    departure_time: datetime
    luggage: bool
    assigned_employees: List[EmployeeOut]  # Здесь можно хранить сериализованный JSON

    class Config:
        orm_mode = True


class RequestSchema(BaseModel):
    id: int
    departure_station: StationBase
    arrival_station: StationBase
    departure_time: datetime
    passenger_type: str
    status: str
    luggage: bool

    class Config:
        orm_mode = True

class EmergencyRequestIn(BaseModel):
    request_id: int
    message: str

class ReassignRequestSchema(BaseModel):
    request_id: int
    employee_ids: List[int]

class UserOut(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class StationCreate(StationBase):
    pass

class Station(StationBase):
    id: int

    class Config:
        orm_mode = True

class DisruptionBase(BaseModel):
    station_id: int
    type: str
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime

class DisruptionCreate(DisruptionBase):
    pass

class DisruptionOut(DisruptionBase):
    id: int
    created_at: datetime
    station: StationBase  # Вложенный объект станции

    class Config:
        orm_mode = True


class ScheduleBase(BaseModel):
    employee_id: int
    start_time: datetime
    end_time: datetime
    is_available: Optional[bool] = True

class ScheduleCreate(ScheduleBase):
    pass

class Schedule(ScheduleBase):
    id: int

    class Config:
        orm_mode = True
