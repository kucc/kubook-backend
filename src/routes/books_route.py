from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from dependencies import get_db
from domain.schemas.book_schemas import DomainReqGetBook
from domain.services.book_service import service_read_book, service_search_books
from routes.response.book_response import RouteResGetBook, RouteResGetBookList

router = APIRouter(
    prefix="/books",
    tags=["books"]
)


@router.get(
    "/{book_id}",
    summary="책 정보 조회",
    response_model=RouteResGetBook,
    status_code=status.HTTP_200_OK
)
async def get_book_by_book_id(
    book_id: int,
    db: Session = Depends(get_db),
):
    domain_req = DomainReqGetBook(book_id)
    domain_res = await service_read_book(domain_req, db)
    result = RouteResGetBook(
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
        donor_name=domain_res.donor_name,
        book_status=domain_res.book_status
    )

    return result


@router.get(
    "",
    summary="도서 검색",
    response_model=RouteResGetBookList,
    status_code=status.HTTP_200_OK
)
async def search_books(
    searching_keyword: str = Query(alias="search"),
    db: Session = Depends(get_db)
):
    domain_res = await service_search_books(searching_keyword, db)
    result = RouteResGetBookList(data=domain_res, count=len(domain_res))

    return result
