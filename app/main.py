from fastapi import FastAPI
from app.api.login import router as login_router

app = FastAPI()

# รวม Router
app.include_router(login_router)
