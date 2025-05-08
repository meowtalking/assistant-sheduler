from datetime import datetime, timedelta
from collections import defaultdict
from typing import List
from app.models import Request, Employee

MAX_REQUESTS_PER_DAY = 5
TIME_BUFFER = timedelta(hours=2)

# Функции-помощники
def is_employee_available(employee: Employee, departure_time: datetime) -> bool:
    weekday = departure_time.strftime("%a").lower()[:3]  # например, 'mon'
    if weekday not in (employee.available_days or []):
        return False

    shift_start = employee.shift_start  # уже datetime.time
    shift_end = employee.shift_end
    dep_time = departure_time.time()

    return shift_start <= dep_time <= shift_end

def requests_conflict(r1: Request, r2: Request) -> bool:
    delta = abs(r1.departure_time - r2.departure_time)
    return delta < TIME_BUFFER

def assign_employees(requests: List[Request], employees: List[Employee]):
    assigned_requests = []
    daily_load = defaultdict(lambda: defaultdict(int))  # employee_id -> date -> count
    schedule = defaultdict(list)  # employee_id -> List[Request]

    for request in sorted(requests, key=lambda r: r.departure_time):
        # Вычисляем требуемое количество сотрудников
        if request.passenger_type == "blind":
            required = 2 if request.luggage else 1
        elif request.passenger_type == "wheelchair":
            required = 4 if request.luggage else 2
        else:
            required = 1

        available = []

        for employee in employees:
            if request.passenger_type not in (employee.skills or []):
                continue
            if not is_employee_available(employee, request.departure_time):
                continue
            if daily_load[employee.id][request.departure_time.date()] >= MAX_REQUESTS_PER_DAY:
                continue

            # Проверка конфликтов по времени
            if any(requests_conflict(request, assigned) for assigned in schedule[employee.id]):
                continue

            available.append(employee)

        if len(available) >= required:
            assigned = available[:required]
            request.assigned_employees = assigned  # Сохраняем список в объект (для создания в БД)

            for emp in assigned:
                schedule[emp.id].append(request)
                daily_load[emp.id][request.departure_time.date()] += 1

            assigned_requests.append(request)
        else:
            request.assigned_employees = []  # Назначить никого не удалось

    return assigned_requests
