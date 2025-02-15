from fastapi import APIRouter, HTTPException
from app.core.config import supabase
from app.core.security import hash_password, verify_password, create_access_token
from app.schemas.user import RegisterRequest, LoginRequest
from datetime import timedelta

router = APIRouter()

@router.post("/register", tags=["auth"])
async def register(user: RegisterRequest):
    existing_user = supabase.table("users").select("username").eq("username", user.username).execute()
    if existing_user.data:
        raise HTTPException(status_code=400, detail="Username already exists")

    existing_email = supabase.table("users").select("email").eq("email", user.email).execute()
    if existing_email.data:
        raise HTTPException(status_code=400, detail="Email already exists")

    existing_mobile = supabase.table("users").select("mobile").eq("mobile", user.mobile).execute()
    if existing_mobile.data:
        raise HTTPException(status_code=400, detail="Mobile number already exists")

    hashed_password = hash_password(user.password)

    # บันทึกข้อมูลลง Supabase
    supabase.table("users").insert({
        "username": user.username,
        "password": hashed_password,
        "gender": user.gender,
        "email": user.email,
        "mobile": user.mobile
    }).execute()

    return {"message": "User registered successfully"}

@router.post("/login", tags=["auth"])
async def login(user: LoginRequest):
    response = supabase.table("users").select("*").eq("username", user.username).execute()
    if not response.data:
        raise HTTPException(status_code=400, detail="Invalid username or password")

    user_data = response.data[0]
    if not verify_password(user.password, user_data["password"]):
        raise HTTPException(status_code=400, detail="Invalid username or password")

    access_token = create_access_token({"sub": user.username}, expires_delta=timedelta(minutes=30))
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users", tags=["users"])
async def get_all_users():
    try:
        response = supabase.table("users").select("username").execute()
        users = response.data
        return {"users": users}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
