from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session
from models import Request, Employee, SessionLocal
from algorithms import assign_employees

app = FastAPI()


@app.post("/assign/{request_id}")
def assign_employees_to_request(request_id: int, db: Session = SessionLocal()):
    request = db.query(Request).filter(Request.id == request_id).first()
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")

    employees = db.query(Employee).all()
    assigned_employees = assign_employees(request, employees)

    # Обновляем заявку с назначенными сотрудниками
    request.assigned_employee_ids = ','.join([str(employee.id) for employee in assigned_employees])
    db.commit()

    return {"message": "Employees assigned successfully", "assigned_employees": assigned_employees}
