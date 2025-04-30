from fastapi import HTTPException
from app.models import Request, Employee
from app.schemas import RequestOut  # Предположим, что у тебя есть Pydantic схемы
from app.algorithms import assign_employees
from app.database import SessionLocal

from fastapi import WebSocket, WebSocketDisconnect
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.models import Request
from app.schemas import RequestSchema
from app.dependencies import get_db
from typing import List

app = FastAPI()

@app.get("/api/requests", response_model=List[RequestSchema])
def get_requests(db: Session = Depends(get_db)):
    return db.query(Request).all()

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message received: {data}")
    except WebSocketDisconnect:
        print("Client disconnected")

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.post("/assign/{request_id}")
def assign_employees_to_request(request_id: int, db: Session = Depends(SessionLocal)):
    request = db.query(Request).filter(Request.id == request_id).first()
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")

    employees = db.query(Employee).all()
    assigned_employees = assign_employees(request, employees)

    # Обновляем заявку с назначенными сотрудниками
    request.assigned_employee_ids = ','.join([str(employee.id) for employee in assigned_employees])
    db.commit()

    return {"message": "Сотрудники назначены успешно", "assigned_employees": assigned_employees}

@app.get("/assign/{id}")
async def get_task(id: int):
    # Обработка GET-запроса
    return {"message": f"Task {id} details"}


@app.get("/api/schedule")
def get_schedule():
    # Пример данных
    return [
        {"id": 1, "name": "Иван Иванов", "shift_time": "09:00-18:00"},
        {"id": 2, "name": "Мария Петрова", "shift_time": "10:00-19:00"}
    ]

@app.get("/api/requests")
def get_requests():
    # Пример данных
    return [
        {"id": 1, "passenger_type": "VIP", "departure_station": "A", "arrival_station": "B", "status": "Pending"},
        {"id": 2, "passenger_type": "Regular", "departure_station": "C", "arrival_station": "D", "status": "Completed"}
    ]
