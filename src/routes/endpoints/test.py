from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from core.database import get_db


from repositories import user as user_repository

router = APIRouter(
    prefix="/test",
    tags=["test"]
)


class UserResponse(BaseModel):
    id: int
    email: str
    is_active: bool


@router.get("/users", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db)):
    users = db.query(user_repository.User).all()
    # ListUserReponse로 변환
    user_response_list = []
    for user in users:
        user_response = UserResponse(
            id=user.id,
            email=user.email,
            is_active=user.is_active,
        )
        user_response_list.append(user_response)
    return user_response_list
