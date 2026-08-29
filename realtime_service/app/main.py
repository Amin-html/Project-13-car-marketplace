from fastapi import FastAPI
from app.core import django_setup  # noqa: F401
from app.ws import chat

app = FastAPI(title="Car Marketplace Realtime")
app.include_router(chat.router)

@app.get("/health")
async def health():
    return {"status": "ok"}