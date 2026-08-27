FROM python:3.13-slim
WORKDIR /app

# Сначала копируем и устанавливаем зависимости (для лучшего кэширования Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Затем копируем остальной код приложения
COPY . .
