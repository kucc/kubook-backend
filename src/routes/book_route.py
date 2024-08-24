from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from dependencies import get_db

# from domain.schemas.book_schemas import BookSearchResult

router = APIRouter(
    prefix="/books",
    tags=["books"]
)


@router.get(
    "/search",
    # response_model=List[BookSearchResult],
    summary="도서 검색",
    description="""
    - 도서 제목, 저자, ISBN으로 검색
    - 검색 결과는 도서 제목, 저자, ISBN만 표시
    - 검색 결과가 없을 경우 빈 배열 반환
    """,
    response_description={
        200: {"description": "Search successful"},
        404: {"description": "No books found"}
    }
)
async def search_books(db: Session = Depends(get_db)):
    pass


@router.get(
    "/categories/{category_id}",
    summary="카테고리별 도서 조회",
)
async def list_books_by_category(db: Session = Depends(get_db)):
    pass
