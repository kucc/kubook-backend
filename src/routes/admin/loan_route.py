from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from dependencies import get_current_active_user, get_db
from domain.services.admin.loan_service import service_admin_read_loans
from routes.admin.response.loan_response import RouteResAdminGetLoanList

router = APIRouter(
    prefix="/admin/loans",
    tags=["admin"],
    dependencies=[Depends(get_current_active_user)]
)
"""
    get_current_admin이 미완성이라 get_current_active_user에 의존성 주입함.
"""

@router.get(
    "",
    response_model=RouteResAdminGetLoanList,
    status_code=status.HTTP_200_OK,
    summary="전체 대출 목록 조회",
)
async def get_all_loans(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user)
):
    response = await service_admin_read_loans(db)

    return response
