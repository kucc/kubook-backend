from typing import Annotated

from fastapi import APIRouter, Depends, Path, status
from sqlalchemy.orm import Session

from dependencies import get_current_admin, get_db
from domain.schemas.loan_schemas import DomainResGetLoan
from domain.services.admin.loan_service import service_admin_toggle_loan_return

router = APIRouter(
    prefix="/admin/loans",
    tags=["admin/loans"],
    dependencies=[Depends(get_current_admin)]
)


@router.put(
    "/return/{loan_id}",
    response_model=DomainResGetLoan,
    status_code=status.HTTP_200_OK,
    summary="관리자의 대출 반납 상태 수정"
)
async def toggle_loan(
    loan_id: Annotated[int, Path(description="대출 정보 id", gt=0)],
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    response = await service_admin_toggle_loan_return(loan_id, db)

    return response
