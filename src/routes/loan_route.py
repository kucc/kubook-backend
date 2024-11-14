from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from dependencies import get_current_active_user, get_db
from domain.schemas.loan_schemas import DomainReqPostLoan, DomainReqPutLoan, DomianResGetLoanItem
from domain.services.loan_service import service_create_loan, service_extend_loan
from routes.request.loan_request import RouteReqPostLoan
from routes.response.loan_response import RouteResPostLoan

router = APIRouter(
    prefix="/loans",
    tags=["loans"],
    dependencies=[Depends(get_current_active_user)]
)


@router.post(
    "",
    response_model=RouteResPostLoan,
    status_code=status.HTTP_200_OK,
    summary="대출 신청"
)
async def create_loan(
    route_req: RouteReqPostLoan,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user)
):
    domain_req = DomainReqPostLoan(
        user_id=current_user.id,
        book_id=route_req.book_id
    )
    result = await service_create_loan(domain_req, db)
    return result


@router.put(
    "/{loan_id}/extend",
    response_model=DomianResGetLoanItem,
    status_code=status.HTTP_200_OK,
    summary="대출 연장",
)
async def extend_loan(
    loan_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user)
):
    domain_req = DomainReqPutLoan(
        loan_id=loan_id,
        user_id=current_user.id
    )
    result = await service_extend_loan(domain_req, db)
    return result
