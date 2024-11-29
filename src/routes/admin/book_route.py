from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from dependencies import get_current_admin, get_db
from domain.schemas.book_schemas import DomainReqAdminDelBook, DomainReqAdminPostBook, DomainReqAdminPutBook
from domain.services.admin.book_service import (
    service_admin_create_book,
    service_admin_delete_book,
    service_admin_read_books,
    service_admin_search_books,
    service_admin_update_book,
)
from routes.admin.request.book_request import RouteReqAdminPostBook, RouteReqAdminPutBook
from routes.admin.response.book_response import RouteResAdminGetBookList, RouteResAdminPostBook, RouteResAdminPutBook

router = APIRouter(
    prefix="/admin/books",
    tags=["admin/books"],
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
):
    response = await service_admin_read_books(
        db=db
    )

    result = RouteResAdminGetBookList(
            data=response,
            count=len(response)
    )

    return result


@router.post(
    "/",
    summary="관리자 도서 정보 등록",
    response_model=RouteResAdminPostBook,
    status_code=status.HTTP_201_CREATED
)
async def create_admin_book(
    request: RouteReqAdminPostBook,
    db: Session = Depends(get_db),
):
    domain_req = DomainReqAdminPostBook(
      book_title = request.book_title,
      code=request.code,
      category_name = request.category_name,
      subtitle=request.subtitle,
      author=request.author,
      publisher=request.publisher,
      publication_year=request.publication_year,
      image_url = request.image_url,
      version = request.version,
      major = request.major,
      language=request.language,
      book_status=request.book_status,
      donor_name = request.donor_name
    )
    domain_res = await service_admin_create_book(domain_req, db)
    result = RouteResAdminPostBook(
        book_id=domain_res.book_id,
        book_title=domain_res.book_title,
        code=domain_res.code,
        category_name=domain_res.category_name,
        subtitle=domain_res.subtitle,
        author=domain_res.author,
        publisher=domain_res.publisher,
        publication_year=domain_res.publication_year,
        image_url=domain_res.image_url,
        version=domain_res.version,
        major=domain_res.major,
        language=domain_res.language,
        book_status=domain_res.book_status,
        donor_name=domain_res.donor_name,
        created_at=domain_res.created_at,
        updated_at=domain_res.updated_at
    )
    return result


@router.put(
    "/{book_id}",
    summary="관리자 도서 정보 수정",
    response_model=RouteResAdminPutBook,
    status_code=status.HTTP_200_OK
)
async def update_admin_book(
    book_id: int,
    request: RouteReqAdminPutBook,
    db: Session = Depends(get_db),
):
    domain_req = DomainReqAdminPutBook(
        book_id= book_id,
        book_title = request.book_title,
        code=request.code,
        category_name = request.category_name,
        subtitle=request.subtitle,
        author=request.author,
        publisher=request.publisher,
        publication_year=request.publication_year,
        image_url = request.image_url,
        version = request.version,
        major = request.major,
        language=request.language,
        book_status=request.book_status,
        donor_name = request.donor_name
    )
    domain_res = await service_admin_update_book(domain_req, db)
    result = RouteResAdminPutBook(
        book_id=domain_res.book_id,
        book_title=domain_res.book_title,
        code=domain_res.code,
        category_name=domain_res.category_name,
        subtitle=domain_res.subtitle,
        author=domain_res.author,
        publisher=domain_res.publisher,
        publication_year=domain_res.publication_year,
        image_url=domain_res.image_url,
        version=domain_res.version,
        major=domain_res.major,
        language=domain_res.language,
        book_status=domain_res.book_status,
        donor_name=domain_res.donor_name,
        created_at=domain_res.created_at,
        updated_at=domain_res.updated_at
    )
    return result

@router.delete(
    "/{book_id}",
    summary="관리자 도서 정보 등록",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_admin_book(
    book_id: int,
    db: Session = Depends(get_db),
):
    domain_req = DomainReqAdminDelBook(
      book_id=book_id
    )
    await service_admin_delete_book(domain_req, db)
    return
