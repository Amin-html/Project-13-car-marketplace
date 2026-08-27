from fastapi import FastAPI
from app.core import django_setup  # noqa: F401 — важен сам факт импорта, до любых других импортов Django-моделей
from app.routers import auth, listings, deals

app = FastAPI(title="Car Marketplace API")
app.include_router(auth.router)
app.include_router(listings.router)
app.include_router(deals.router)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/debug/listings-count")
async def listings_count():
    from listings.models import Listing
    from asgiref.sync import sync_to_async

    count = await sync_to_async(Listing.objects.count)()
    return {"listings": count}