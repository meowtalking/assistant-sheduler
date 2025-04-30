from fastapi import HTTPException
from app.models import Request, Employee
from app.schemas import RequestOut  # Предположим, что у тебя есть Pydantic схемы
from app.algorithms import assign_employees
from app.database import SessionLocal

from fastapi import WebSocket, WebSocketDisconnect
from app.models import Request
from app.schemas import RequestSchema
from app.dependencies import get_db
from typing import List
from fastapi import FastAPI, Depends, HTTPException
from . import models, database, schemas, auth, dependencies
from sqlalchemy.orm import Session

app = FastAPI()
app.include_router(auth.router)

models.Base.metadata.create_all(bind=database.engine)


@app.post("/requests", tags=["requests"])
def create_request(request: schemas.RequestCreate, db: Session = Depends(dependencies.get_db),
                   current_user=Depends(dependencies.get_current_user)):
    if not current_user.is_disabled:
        raise HTTPException(status_code=403,
                            detail="Заявки может подавать только пользователь с ограниченными возможностями")

    new_request = models.Request(
        user_id=current_user.id,
        departure_station=request.departure_station,
        arrival_station=request.arrival_station,
        departure_time=request.departure_time,
    )
    db.add(new_request)
    db.commit()
    db.refresh(new_request)
    return {"message": "Заявка подана", "request_id": new_request.id}


@app.get("/api/requests", response_model=List[RequestSchema])
def get_requests(db: Session = Depends(get_db)):
    return db.query(Request).all()



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

