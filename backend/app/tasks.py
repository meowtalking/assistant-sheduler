from celery import Celery
from datetime import datetime

app = Celery('tasks', broker='redis://localhost:6379/0')

@app.task
def reassign_employees(request_id: int):
    # Логика перераспределения сотрудников
    print(f"Reassigning employees for request {request_id} at {datetime.now()}")
    # Реализуйте перераспределение сотрудников по заявке
    return f"Request {request_id} reassigned."
