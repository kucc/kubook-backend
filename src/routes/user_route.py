from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from dependencies import get_current_active_user, get_db

from response.loan_response import LoanListResponse
from domain.services.loan_service import get_all_user_loans as service_get_all_user_loans

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
    response_model=LoanListResponse,
    status_code=status.HTTP_200_OK,
    summary="회원의 전체 대출 목록 조회",
)
async def get_all_user_loans(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user)
):
    result = await service_get_all_user_loans(current_user.id, db)

    response = LoanListResponse(
        data=result,
        count=len(result)
    )
    return response
