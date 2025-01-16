from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import User
from database import get_db

app = FastAPI()

@app.get("/users/")
async def get_users(db: AsyncSession = Depends(get_db)):
    # ดึงข้อมูลผู้ใช้ทั้งหมดจาก Table users
    result = await db.execute(select(User))
    users = result.scalars().all()
    return users

@app.get("/users/{user_id}")
async def get_user(user_id: str, db: AsyncSession = Depends(get_db)):
    # ดึงข้อมูลผู้ใช้ตาม ID
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
