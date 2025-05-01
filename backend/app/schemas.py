from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class RequestCreate(BaseModel):
    departure_station: str
    arrival_station: str
    departure_time: datetime

class RequestOut(BaseModel):
    id: int
    status: str
    departure_station: str
    arrival_station: str

    class Config:
        orm_mode = True

class RequestSchema(BaseModel):
    id: int
    departure_station: str
    arrival_station: str
    departure_time: datetime
    passenger_type: Optional[str]
    status: Optional[str]
    luggage: Optional[bool]
    assigned_employee_ids: Optional[str]

    class Config:
        orm_mode = True


class UserOut(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str


class Config:
    orm_mode = True  # Это позволяет конвертировать объекты SQLAlchemy в Pydantic модели
