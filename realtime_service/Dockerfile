FROM python:3.13-slim
WORKDIR /app

RUN pip install --no-cache-dir fastapi uvicorn[standard] websockets redis pyjwt==2.10.1

COPY . .
