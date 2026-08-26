from pydantic import BaseModel, Field
from decimal import Decimal
from datetime import datetime
from typing import Optional

class ListingCreate(BaseModel):
    brand: str
    model: str
    year: int
    mileage: int
    price: Decimal
    condition: str  # "new" | "used"
    vin: Optional[str] = None
    city: str

class ListingOut(BaseModel):
    id: int
    brand: str
    model: str
    year: int
    mileage: int
    price: Decimal
    condition: str
    status: str
    city: str
    seller_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class ListingListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    results: list[ListingOut]