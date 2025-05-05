from datetime import datetime
from pydantic import BaseModel
from typing import Optional

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

class RequestCreate(BaseModel):
    user_id: int
    passenger_type: Optional[str]
    departure_station: str
    arrival_station: str
    departure_time: datetime
    luggage: Optional[bool] = False

class RequestOut(BaseModel):
    id: int
    status: str
    departure_station: str
    arrival_station: str

    class Config:
        orm_mode = True

from typing import Optional, List
from pydantic import BaseModel

class RequestSchema(BaseModel):
    id: int
    departure_station: str
    arrival_station: str
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


