from datetime import date

from fastapi import Depends, Header, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.sql import and_

from database import get_db_session
from domain.services.token_service import verify_jwt
from repositories.models import User


def get_db():
    try:
        session = get_db_session()
        yield session
    finally:
        session.close()

async def get_current_user(token:str=Header(None), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or Expired Access token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if not token:
        raise credentials_exception
    try:
        user_id = verify_jwt(token)
        if user_id < 0:
            raise credentials_exception
        stmt = select(User).where(and_(User.id == user_id, User.is_deleted==False))
        user = db.execute(stmt).scalar_one()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user
    except HTTPException as err:
        raise err


def get_current_active_user(user: User = Depends(get_current_user)):
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    return user


def get_current_admin(user: User = Depends(get_current_user)):
    """
        get_current_admin 사용법 예시

        def example(current_user: User = Depends(get_current_admin)):
            return {"message": "Welcome Admin!"}
    """
    if not user.admin or not user.admin[-1].admin_status or user.admin[-1].is_deleted:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges"
        )
    if user.admin[0].expiration_date < date.today():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user's admin status has expired"
        )
    return user
