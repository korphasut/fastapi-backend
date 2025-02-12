from fastapi import FastAPI
from app.api import protected

app = FastAPI()

app.include_router(protected.router)

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}
