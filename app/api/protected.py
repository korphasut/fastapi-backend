from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.session import get_db
from app.db.models import User

router = APIRouter()

@router.get("/users", response_model=list[str])
async def get_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User.username))
    usernames = [row[0] for row in result.all()]
    return usernames
