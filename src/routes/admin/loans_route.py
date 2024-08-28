from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

import domain.schemas.admin_schemas as s
from dependencies import get_current_admin, get_db
from src.utils.admin_service import *
from repositories.loan_repository import Loan

router = APIRouter(
    prefix="/admin/loan",
    tags=["admin/loan"],
    dependencies=[Depends(get_current_admin)]
)


@router.get(
    "/",
    summary="전체 대출 목록 조회",
    response_model=List[s.LoanRes],
    status_code=status.HTTP_200_OK
)
async def get_list_loans(db: Session = Depends(get_db)):
    return get_list(Loan, db)


@router.get(
    "/{loan_id}",
    summary="대출 정보 조회",
    response_model=s.LoanRes,
    status_code=status.HTTP_200_OK
)
async def get_loan(loan_id: int,  db: Session = Depends(get_db)):
    return get_item(Loan, loan_id, db)


@router.patch(
    "/{loan_id}",
    summary="대출 정보 수정",
    response_model=s.LoanRes,
    status_code=status.HTTP_200_OK
)
async def update_loan(loan_id: int, loan: LoanUpdate,  db: Session = Depends(get_db)):
    return update_item(Loan, loan_id, loan, db)


@router.delete(
    "/{loan_id}",
    summary="대출 정보 삭제",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_loan(loan_id: int,  db: Session = Depends(get_db)):
    return delete_item(Loan, loan_id, db)


@router.patch(
    "/{loan_id}/return",
    summary="반납 승인",
    response_model=s.LoanRes,
    status_code=status.HTTP_200_OK
)
async def return_loan(loan_id: int, return_date: date | None,  db: Session = Depends(get_db)):
    if (return_date == None):
        return_date = date.today()

    loan: LoanUpdate = {
        "return_status": True,
        "return_date": return_date
    }
    return update_item(Loan, loan_id, loan, db)
