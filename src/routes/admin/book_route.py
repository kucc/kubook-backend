from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from dependencies import get_current_admin, get_db
from domain.services.admin.book_service import service_admin_read_books, service_admin_search_books
from routes.admin.response.book_response import RouteResAdminGetBookList

router = APIRouter(
    prefix="/admin/books",
    tags=["admin"],
    dependencies=[Depends(get_current_admin)]
)


@router.get(
    "/search",
    response_model=RouteResAdminGetBookList,
    status_code=status.HTTP_200_OK,
    summary="전체 도서 목록 검색",
)
async def search_books(
    db: Session = Depends(get_db),
    book_title: Annotated[
        str | None, Query(description="도서 제목", example="book", min_length=2, max_length=50)
    ] = None,
    category_name: Annotated[
        str | None, Query(description="카테고리 이름", example="category", min_length=2, max_length=50)
    ] = None,
    author: Annotated[
        str, Query(description="저자", example="author", min_length=2, max_length=50)
    ] = None,
    publisher: Annotated[
        str, Query(description="출판사", example="publisher", min_length=2, max_length=50)
    ] = None,
    return_status: Annotated[
        bool, Query(description="반납 여부", example=False)
    ] = None,
    current_user=Depends(get_current_admin)
):

    response = await service_admin_search_books(
        book_title=book_title,
        category_name=category_name,
        author=author,
        publisher=publisher,
        return_status=return_status,
        db=db
    )

    result = RouteResAdminGetBookList(
            data=response,
            count=len(response)
    )

    return result


@router.get(
    "/",
    response_model=RouteResAdminGetBookList,
    status_code=status.HTTP_200_OK,
    summary="전체 도서 목록 조회",
)
async def get_all_books(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_admin)
):
    response = await service_admin_read_books(
        db=db
    )

    result = RouteResAdminGetBookList(
            data=response,
            count=len(response)
    )

    return result
