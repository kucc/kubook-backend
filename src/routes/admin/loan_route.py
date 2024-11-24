from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from dependencies import get_current_admin, get_db
from domain.services.admin.loan_service import service_admin_search_loans
from routes.admin.response.loan_response import RouteResAdminGetLoanList

router = APIRouter(
    prefix="/admin/loans",
    tags=["admin"],
    dependencies=[Depends(get_current_admin)]
)

@router.get(
    "/search",
    response_model=RouteResAdminGetLoanList,
    status_code=status.HTTP_200_OK,
    summary="전체 대출 목록 검색",
)
async def search_loans(
    user_name: Annotated[
        str | None, Query(description="사용자 이름", example="test", min_length=2, max_length=45)
    ] = None,
    book_title: Annotated[
        str, Query(description="도서 제목", example="book", min_length=2, max_length=50)
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

    return response



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
    response = await service_admin_search_loans(
        db = db
    )

    return response
