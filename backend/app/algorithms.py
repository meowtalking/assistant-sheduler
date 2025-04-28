from models import Employee, Request

def assign_employees(request: Request, employees: list[Employee]):
    required_employees = 1 if request.passenger_type == "слабовидящий" else 2
    available_employees = []

    # Фильтруем сотрудников, которые могут работать с данным типом пассажира
    for employee in employees:
        if request.passenger_type in employee.skills:
            available_employees.append(employee)

    # Распределяем сотрудников на заявку
    assigned_employees = available_employees[:required_employees]
    return assigned_employees
