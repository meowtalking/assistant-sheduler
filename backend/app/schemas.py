
from pydantic import BaseModel
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

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

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str


class RequestOut(BaseModel):
    id: int
    passenger_type: str
    departure_station: str
    arrival_station: str
    departure_time: str
    status: str
    luggage: bool
    assigned_employee_ids: str

class Config:
    orm_mode = True  # Это позволяет конвертировать объекты SQLAlchemy в Pydantic модели
