from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models import User, Token
from app.db.session import get_db
from app.schemas.user import LoginRequest
from app.core.security import create_access_token
from datetime import datetime, timedelta, timezone

router = APIRouter()

@router.post("/login/")
async def login(request: LoginRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.username == request.username))
    user = result.scalars().first()

    if not user or user.password != request.password:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # สร้าง JWT Token
    access_token_expires = timedelta(minutes=30)
    token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)

    # บันทึก Token ลง Database
    expires_at = (datetime.now(timezone.utc) + access_token_expires).replace(tzinfo=None)
    new_token = Token(user_id=user.id, token=token, expires_at=expires_at)
    db.add(new_token)
    await db.commit()

    return {"message": "Login successful", "access_token": token, "token_type": "bearer"}

@router.get("/users/")
async def get_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    users = result.scalars().all()
    return users

@router.get("/users/{username}")
async def get_user(username: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
