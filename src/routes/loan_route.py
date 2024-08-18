from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from dependencies import get_current_active_user, get_db
import domain.schemas.loan_schemas as loan_schemas
import domain.services.loan_service as loan_service
router = APIRouter(
    prefix="/loans",
    tags=["loans"]
)


@router.post(
    "/",
    summary="도서 대출 신청",
)
async def create_loan(db: Session = Depends(get_db), current_user=Depends(get_current_active_user)):
    pass


@router.get(
    "/",
    summary="대출 목록 조회",
)
async def list_loans(db: Session = Depends(get_db), current_user=Depends(get_current_active_user)):
    pass


@router.get(
    "/{loan_id}",
    summary="대출 상세 정보 조회",
)
async def get_loan(db: Session = Depends(get_db), current_user=Depends(get_current_active_user)):
    pass


@router.put(
    "/{loan_id}",
    summary="대출 정보 수정 (연장 등)",
)
async def update_loan(db: Session = Depends(get_db), current_user=Depends(get_current_active_user)):
    pass


@router.delete(
    "/{loan_id}",
    summary="대출 정보 삭제 (반납 처리)",
)
async def delete_loan(db: Session = Depends(get_db), current_user=Depends(get_current_active_user)):
    pass


@router.put(
    "/{loan_id}/extend",
    response_model=loan_schemas.LoanExtendResponse,
    status_code=status.HTTP_200_OK,
    summary="대출 연장",
)
async def extend_loan(loan_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_active_user)):
    return await loan_service.extend_loan(current_user, loan_id, db)
