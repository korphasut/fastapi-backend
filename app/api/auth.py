from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.session import get_db
from app.db.models import User
from app.schemas.user import UserCreate, Token
from app.core.security import verify_password, get_password_hash, create_access_token
from datetime import timedelta

router = APIRouter()

@router.post("/register", response_model=Token)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    async with db as session:
        result = await session.execute(select(User).filter(User.username == user_data.username))
        existing_user = result.scalars().first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already taken")

        hashed_password = get_password_hash(user_data.password)
        new_user = User(username=user_data.username, password=hashed_password)
        session.add(new_user)
        await session.commit()

        access_token = create_access_token(data={"sub": new_user.username})
        return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
async def login(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    async with db as session:
        result = await session.execute(select(User).filter(User.username == user_data.username))
        user = result.scalars().first()
        if not user or not verify_password(user_data.password, user.password):
            raise HTTPException(status_code=400, detail="Invalid credentials")

        access_token = create_access_token(data={"sub": user.username})
        return {"access_token": access_token, "token_type": "bearer"}
