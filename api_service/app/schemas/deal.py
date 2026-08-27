from pydantic import BaseModel
from datetime import datetime

class DealCreate(BaseModel):
    listing_id: int

class DealStatusUpdate(BaseModel):
    status: str  # "negotiating" | "confirmed" | "completed" | "cancelled"

class DealOut(BaseModel):
    id: int
    listing_id: int
    buyer_id: int
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True