from pydantic import BaseModel, EmailStr, StringConstraints
from typing import Annotated, Literal

class RegisterRequest(BaseModel):
    username: Annotated[str, StringConstraints(min_length=3, max_length=20)]
    password: Annotated[str, StringConstraints(min_length=6)]
    gender: Literal["male", "female", "other"]
    email: EmailStr
    mobile: Annotated[str, StringConstraints(min_length=10, max_length=15)]

class LoginRequest(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: str
    username: str
    gender: str
    email: str
    mobile: str

    model_config = {
        "from_attributes": True
    }
