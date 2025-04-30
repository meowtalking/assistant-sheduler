# Используем Node.js для фронтенда
FROM node:16

# Устанавливаем рабочую директорию
WORKDIR /frontend

# Копируем package.json и устанавливаем зависимости
COPY package.json /frontend/
RUN npm install

# Копируем все остальные файлы
COPY . /frontend/

# Указываем порт, на котором будет работать приложение
EXPOSE 3000

# Запускаем приложение
CMD ["npm", "start"]
