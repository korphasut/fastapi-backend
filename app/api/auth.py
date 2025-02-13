from fastapi import APIRouter, HTTPException, Depends
from app.core.config import supabase

router = APIRouter()

@router.get("/users", tags=["users"])
async def get_all_users():
    try:
        response = supabase.table("users").select("username").execute()
        users = response.data
        return {"users": users}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
