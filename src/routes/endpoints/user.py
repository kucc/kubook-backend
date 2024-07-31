from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

"""
- GET /users/{user_id}: 사용자 정보 조회
- PUT /users/{user_id}: 사용자 정보 수정
- DELETE /users/{user_id}: 사용자 정보 삭제
"""
