from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
import os
from app.core.config import SUPABASE_URL, SUPABASE_KEY

DATABASE_URL = f"postgresql://postgres:{SUPABASE_KEY}@{SUPABASE_URL.replace('https://', '')}/postgres"

Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
