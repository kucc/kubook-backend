from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from dependencies import get_current_active_user, get_db
from domain.schemas.loan_schemas import DomianResGetLoanItem
from domain.services.admin.loan_service import service_admin_return_loan

router = APIRouter(
    prefix="/admin/loans",
    tags=["admin/loans"],
    dependencies=[Depends(get_current_active_user)]
)


@router.put(
    "/{loan_id}/toggle",
    response_model=DomianResGetLoanItem,
    status_code=status.HTTP_200_OK,
    summary="관리자의 대출 반납 수정"
)
async def return_loan(
    loan_id: int,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_active_user),
):
    response = await service_admin_return_loan(loan_id, db)

    return response
