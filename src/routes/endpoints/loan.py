from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.core.dependencies import get_db, get_current_active_user

router = APIRouter(
    prefix="/loans",
    tags=["loans"]
)

"""
- POST /loans: 도서 대출 신청
- GET /loans: 대출 목록 조회
- GET /loans/{loan_id}: 대출 상세 정보 조회
- PUT /loans/{loan_id}: 대출 정보 수정 (연장 등)
- DELETE /loans/{loan_id}: 대출 정보 삭제 (반납 처리)
"""


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
