from sqlalchemy import Column, String, Text
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.db.session import Base

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    username = Column(String(20), unique=True, nullable=False)
    password = Column(Text, nullable=False)
    gender = Column(String(10), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    mobile = Column(String(15), unique=True, nullable=False)