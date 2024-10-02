from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from dependencies import get_db
from domain.schemas.bookinfo_schemas import ReqeustGetBookInfo
from domain.services.book_service import service_search_books
from domain.services.bookinfo_service import read_bookinfo as service_read_bookinfo
from routes.response.book_response import RouteResGetBookList
from routes.response.bookinfo_response import BookInfoResponse

router = APIRouter(
    prefix="/books",
    tags=["books"]
)


@router.get(
    "/{bookinfo_id}",
    summary="도서 상세 정보 조회",
    response_model=BookInfoResponse,
    status_code=status.HTTP_200_OK
)
async def get_bookinfo(
    bookinfo_id: int,
    db: Session = Depends(get_db),
):
    domain_req = ReqeustGetBookInfo(bookinfo_id=bookinfo_id)
    domain_res = await service_read_bookinfo(domain_req, db)
    result = BookInfoResponse(
        bookinfo_id=domain_res.bookinfo_id,
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
        language=domain_res.language
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
    result = RouteResGetBookList(
        data=domain_res,
        count=len(domain_res)
    )

    return result
