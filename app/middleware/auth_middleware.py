from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from app.core.config import settings

async def get_current_user(token: str = Depends(lambda: None)):
    credentials_exception = HTTPException(status_code=401, detail="Invalid credentials")
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return {"sub": username}
    except JWTError:
        raise credentials_exception
