from fastapi import FastAPI
from app.api.login import router as login_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# รวม Router
app.include_router(login_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # หรือกำหนดเฉพาะ URL ที่อนุญาต
    allow_credentials=True,
    allow_methods=["*"],  # อนุญาตทุก method เช่น GET, POST
    allow_headers=["*"],  # อนุญาตทุก headers
)