from datetime import date

from config import Settings
from database import get_db_session
from fastapi import Depends, Header, HTTPException, status
from jose import JWTError, jwt
from models import User
from sqlalchemy.orm import Session


def get_db():
    try:
        session = get_db_session()
        yield session
    finally:
        session.close()


async def get_current_user(token=Header(None), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = jwt.decode(token, key=Settings().JWT_SECRET_KEY, algorithms=Settings().JWT_ALGORITHM)
    user_id: int = int(payload.get("sub"))
    if user_id is None:
        raise credentials_exception
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    if not user.is_valid:
        raise credentials_exception
    return user


def get_current_active_user(user: User = Depends(get_current_user)):
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return user


def get_current_admin(user: User = Depends(get_current_active_user)):
    if not user.admin or not user.admin.admin_status or not user.admin.is_valid:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges"
        )
    if user.admin.expiration_date < date.today():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user's admin status has expired"
        )
    return user


"""
get_current_admin 사용법 예시

def example(current_user: User = Depends(get_current_admin)):
    return {"message": "Welcome Admin!"}
"""
