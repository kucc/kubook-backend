from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query, status
from sqlalchemy.orm import Session

from dependencies import get_current_admin, get_db
from domain.schemas.loan_schemas import DomainResGetLoan
from domain.services.admin.loan_service import service_admin_read_loans, service_admin_search_loans, service_admin_toggle_loan_return
from routes.admin.response.loan_response import RouteResAdminGetLoanList


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

  
@router.get(
    "/search",
    response_model=RouteResAdminGetLoanList,
    status_code=status.HTTP_200_OK,
    summary="전체 대출 목록 검색",
)
async def search_loans(
    book_title: Annotated[
        str, Query(description="도서 제목", example="book", min_length=2, max_length=50)
    ] = None,
    user_name: Annotated[
        str | None, Query(description="사용자 이름", example="test", min_length=2, max_length=45)
    ] = None,
    category_name: Annotated[
        str, Query(description="카테고리 이름", example="category", min_length=2, max_length=50)
    ] = None,
    return_status: Annotated[
        bool, Query(description="반납 여부", example=False)
    ] = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_admin)
):
    response = await service_admin_search_loans(
        user_name = user_name,
        book_title = book_title,
        category_name = category_name,
        return_status = return_status,
        db = db
    )

    result = RouteResAdminGetLoanList(
            data=response,
            count=len(response)
        )

    return result



@router.get(
    "/",
    response_model=RouteResAdminGetLoanList,
    status_code=status.HTTP_200_OK,
    summary="전체 대출 목록 조회",
)
async def get_all_loans(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_admin)
):
    response = await service_admin_read_loans(
        db = db
    )

    result = RouteResAdminGetLoanList(
            data=response,
            count=len(response)
        )

    return result

