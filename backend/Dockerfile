# Используем Python 3.9
FROM python:3.9

# Устанавливаем рабочую директорию
WORKDIR /backend/app

# Копируем зависимости и устанавливаем их
COPY requirements.txt /backend/app/
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install uvicorn

COPY ./backend/wait-for-it.sh /backend/wait-for-it.sh
RUN chmod +x /backend/wait-for-it.sh

# Копируем весь проект в рабочую директорию
COPY . /backend/app/

# Запуск FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
