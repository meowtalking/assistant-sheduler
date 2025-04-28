# Используем Node.js 16
FROM node:16

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем зависимости и устанавливаем их
COPY frontend/package.json frontend/package-lock.json ./
RUN npm install

# Копируем весь проект
COPY frontend/ .

# Запускаем React приложение
CMD ["npm", "start"]
