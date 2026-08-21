from fastapi import APIRouter, HTTPException
from asgiref.sync import sync_to_async
from app.schemas.auth import LoginRequest, TokenResponse
from app.core.security import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest):
    from django.contrib.auth import authenticate

    user = await sync_to_async(authenticate)(
        username=data.username, password=data.password
    )
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(user_id=user.id, role=user.role)
    return TokenResponse(access_token=token)