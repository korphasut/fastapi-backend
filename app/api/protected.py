from fastapi import APIRouter, Depends
from app.middleware.auth_middleware import get_current_user

router = APIRouter()

@router.get("/protected")
async def protected_route(current_user: dict = Depends(get_current_user)):
    return {"message": f"Hello, {current_user['sub']}"}
