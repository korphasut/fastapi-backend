from fastapi import FastAPI
from app.api import auth, protected

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(protected.router, prefix="/protected", tags=["Protected"])