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
    shift_time: str
    skills: str

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
    departure_time: datetime

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
    assigned_employee_ids: Optional[List[int]] = None  # ключевой момент

    class Config:
        orm_mode = True


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
