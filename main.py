from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import User
from database import get_db
from pydantic import BaseModel

class LoginRequest(BaseModel):
    username: str
    password: str

app = FastAPI()

@app.get("/users/")
async def get_users(db: AsyncSession = Depends(get_db)):
    # ดึงข้อมูลผู้ใช้ทั้งหมดจาก Table users
    result = await db.execute(select(User))
    users = result.scalars().all()
    return users

@app.get("/users/{user_name}")
async def get_user(user_name: str, db: AsyncSession = Depends(get_db)):
    # ดึงข้อมูลผู้ใช้ตาม ID
    result = await db.execute(select(User).where(User.username == user_name))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/login/")
async def login(request: LoginRequest, db: AsyncSession = Depends(get_db)):
    # ดึงข้อมูล username และ password จาก Request Body
    username = request.username
    password = request.password

    # ตรวจสอบผู้ใช้ใน Database
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalars().first()

    if not user or user.password != password:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    return {"message": "Login successful", "username": user.username}