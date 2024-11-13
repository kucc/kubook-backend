from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from dependencies import get_current_admin, get_db
from domain.services.admin.book_service import service_admin_read_books
from routes.admin.response.book_response import RouteResAdminGetBookList

router = APIRouter(
    prefix="/admin/books",
    tags=["admin"],
    dependencies=[Depends(get_current_admin)]
)


@router.get(
    "/",
    response_model=RouteResAdminGetBookList,
    status_code=status.HTTP_200_OK,
    summary="전체 도서 목록 조회",
)
async def get_all_loans(
    db: Session = Depends(get_db),
    book_title: str = Query(description="도서 제목", example="book1"),
    current_user=Depends(get_current_admin)
):

    response = await service_admin_read_books(book_title, db)

    return response
