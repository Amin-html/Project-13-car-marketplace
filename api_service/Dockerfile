FROM python:3.13-slim
WORKDIR /app

# Явно перечисляем все пакеты для api_service
RUN pip install --no-cache-dir fastapi uvicorn[standard] django psycopg[binary] asgiref python-dotenv pyjwt==2.10.1

COPY . .
