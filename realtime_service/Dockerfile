FROM python:3.13-slim
WORKDIR /app

# 1. Сначала копируем только файл зависимостей
COPY requirements.txt .

# 2. Устанавливаем все пакеты из файла
RUN pip install --no-cache-dir -r requirements.txt

# 3. Только потом копируем код проекта
COPY . .
