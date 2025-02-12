from fastapi import FastAPI
from app.api import auth, protected

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello from FastAPI + Supabase!"}

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(protected.router, prefix="/protected", tags=["Protected"])