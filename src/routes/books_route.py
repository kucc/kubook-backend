from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from dependencies import get_db
from domain.schemas.book_schemas import DomainReqGetBook
from domain.services.book_service import service_read_book, service_read_books, service_search_books
from routes.response.book_response import RouteResGetBook, RouteResGetBookList

router = APIRouter(
    prefix="/books",
    tags=["books"]
)

@router.get(
    "/search",
    summary="도서 검색",
    response_model=RouteResGetBookList,
    status_code=status.HTTP_200_OK
)
async def search_books(
    search: Annotated[
        str, Query(description="Search Query", min_length=2, max_length=50)
    ] = None,
    is_loanable: Annotated[
        bool, Query(description="대출 가능 여부", example=True)
    ] = None,
    page: Annotated[
        int, Query(description="페이지", example=1, gt=0)
    ] = 1,
    limit: Annotated[
        int, Query(description="페이지 당 조회 개수", example=10, gt=0)
    ] = 10, # 차후 기본 값은 적당히 변경할 예정
    db: Session = Depends(get_db)
) -> RouteResGetBookList:
    domain_res = await service_search_books(
        search=search,
        is_loanable=is_loanable,
        page=page,
        limit=limit,
        db=db
    )
    result = RouteResGetBookList(
        data=domain_res.data,
        count=domain_res.count,
        total=domain_res.total
    )

    return result


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
    domain_req = DomainReqGetBook(book_id=book_id)
    domain_res = await service_read_book(domain_req, db)
    result = RouteResGetBook(
        book_id=domain_res.book_id,
        book_title=domain_res.book_title,
        loanable=domain_res.loanable,
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
        book_status=domain_res.book_status,
        created_at=domain_res.created_at,
        updated_at=domain_res.updated_at
    )

    return result


@router.get(
    "",
    summary="전체 도서 목록 조회",
    response_model=RouteResGetBookList,
    status_code=status.HTTP_200_OK
)
async def get_books(
    page: Annotated[
        int, Query(description="페이지", example=1, gt=0)
    ] = 1,
    limit: Annotated[
        int, Query(description="페이지 당 조회 개수", example=10, gt=0)
    ] = 10, # 차후 기본 값은 적당히 변경할 예정
    db: Session = Depends(get_db)
):
    domain_res = await service_read_books(page, limit, db)
    result = RouteResGetBookList(
        data=domain_res.data,
<<<<<<< HEAD
        count=domain_res.count,
=======
        count=len(domain_res.data),
>>>>>>> 9942b3de2400ca10541f828cf7fb787437736a6c
        total=domain_res.total
    )

    return result
