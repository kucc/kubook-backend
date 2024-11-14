from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from dependencies import get_current_active_user, get_db
from domain.services.loan_service import service_read_loans_by_user_id
from routes.response.loan_response import RouteResGetLoanList

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(get_current_active_user)]
)


@router.get(
    "/{user_id}/loans",
    response_model=RouteResGetLoanList,
    status_code=status.HTTP_200_OK,
    summary="회원의 전체 대출 목록 조회",
)
async def get_all_user_loans(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user)
):
    result = await service_read_loans_by_user_id(current_user.id, db)

    response = RouteResGetLoanList(
        data=result,
        count=len(result)
    )
    return response
