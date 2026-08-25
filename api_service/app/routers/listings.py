from fastapi import APIRouter, Depends
from app.core.dependencies import get_current_user, require_role

router = APIRouter(prefix="/listings", tags=["listings"])

@router.get("/me")
async def whoami(current_user: dict = Depends(get_current_user)):
    return current_user

@router.post("/")
async def create_listing_stub(current_user: dict = Depends(require_role("seller", "admin"))):
    return {"detail": "you are allowed to create listings", "as": current_user}