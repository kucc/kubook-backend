from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from dependencies import get_current_active_user, get_db
from domain.schemas.loan_schemas import LoanItem, LoanExtendRequest, LoanCreateRequest
from domain.services.loan_service import extend_loan as service_extend_loan
from domain.services.loan_service import create_loan as service_create_loan
from routes.response.loan_response import LoanCreateResponse
router = APIRouter(
    prefix="/loans",
    tags=["loans"],
    dependencies=[Depends(get_current_active_user)]
)


@router.post(
    "",
    response_model=LoanCreateResponse,
    status_code=status.HTTP_200_OK,
    summary="대출 신청"
)
async def create_loan(
    book_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user)
):
    domain_req = LoanCreateRequest(
        user_id=current_user.id,
        book_id=book_id
    )
    result = await service_create_loan(domain_req, db)
    return result


@router.put(
    "/{loan_id}/extend",
    response_model=LoanItem,
    status_code=status.HTTP_200_OK,
    summary="대출 연장",
)
async def extend_loan(
    loan_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user)
):
    domain_req = LoanExtendRequest(
        loan_id=loan_id,
        user_id=current_user.id
    )
    result = await service_extend_loan(domain_req, db)
    return result
