from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from backend.core.config import settings
from backend.db.session import SessionLocal
from backend.models.user import User
from backend.crud.crud_user import user as crud_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/login/access-token")

def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=403, detail="Could not validate credentials")
    user = crud_user.get(db, id=token_data)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
