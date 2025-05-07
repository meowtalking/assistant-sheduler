from datetime import datetime, timedelta
from collections import defaultdict
from app.models import Request, Employee

MAX_REQUESTS_PER_DAY = 3  # Ограничение на количество заявок в день

def is_employee_available(employee: Employee, request_time: datetime):
    weekday = request_time.strftime('%a').lower()  # 'mon', 'tue', ...
    if weekday not in employee.available_days:
        return False

    # Проверка смены
    if hasattr(employee, "shift_start") and hasattr(employee, "shift_end"):
        if not (employee.shift_start <= request_time.time() <= employee.shift_end):
            return False

    return True

def requests_overlap(req1: Request, req2: Request):
    delta = timedelta(minutes=30)  # Допустимый интервал между заявками
    return abs(req1.departure_time - req2.departure_time) < delta

def assign_employees(requests: list[Request], employees: list[Employee]):
    assigned_requests = []
    daily_load = defaultdict(lambda: defaultdict(int))  # employee_id -> date -> count
    employee_schedule = defaultdict(list)  # employee_id -> list of assigned requests

    for request in sorted(requests, key=lambda r: r.departure_time):
        # Определяем нужное количество сотрудников
        if request.passenger_type == "слабовидящий":
            required_employees = 1
        elif request.passenger_type == "инвалид-коляска":
            required_employees = 4 if request.luggage else 2
        else:
            required_employees = 1  # По умолчанию

        available_employees = []

        for employee in employees:
            if request.passenger_type not in employee.skills:
                continue
            if not is_employee_available(employee, request.departure_time):
                continue
            if daily_load[employee.id][request.departure_time.date()] >= MAX_REQUESTS_PER_DAY:
                continue

            # Проверка на пересечение заявок
            conflict = False
            for assigned_req in employee_schedule[employee.id]:
                if requests_overlap(request, assigned_req):
                    conflict = True
                    break

            if not conflict:
                available_employees.append(employee)

        if len(available_employees) >= required_employees:
            assigned = available_employees[:required_employees]
            request.assigned_employee_ids = [emp.id for emp in assigned]

            # Обновление графика и нагрузки
            for emp in assigned:
                employee_schedule[emp.id].append(request)
                daily_load[emp.id][request.departure_time.date()] += 1

            assigned_requests.append(request)
        else:
            # Заявку невозможно назначить — можно логировать
            request.assigned_employee_ids = []

    return assigned_requests
