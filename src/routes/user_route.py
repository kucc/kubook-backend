from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from dependencies import get_current_active_user, get_db

import domain.schemas.loan_schemas as user_loan_schemas
import domain.services.loan_service as user_loan_service

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.get(
    "/{user_id}",
    summary="사용자 정보 조회",
)
async def get_user(db: Session = Depends(get_db), current_user=Depends(get_current_active_user)):
    pass


@router.put(
    "/{user_id}",
    summary="사용자 정보 수정",
)
async def update_user(db: Session = Depends(get_db), current_user=Depends(get_current_active_user)):
    pass


@router.delete(
    "/{user_id}",
    summary="사용자 정보 삭제",
)
async def delete_user(db: Session = Depends(get_db), current_user=Depends(get_current_active_user)):
    pass


@router.get(
    "/{user_id}/loans",
    response_model=user_loan_schemas.LoanListResponse,
    status_code=status.HTTP_200_OK,
    summary="전체 대출 목록 조회",
)
async def get_all_user_loans(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user)
):
    return await user_loan_service.get_all_user_loans(current_user, db)
