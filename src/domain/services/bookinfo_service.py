
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from domain.schemas.bookinfo_schemas import BookInfoResponse, ReqeustGetBookInfo
from repositories.models import BookInfo
from utils.crud_utils import get_item


async def read_bookinfo(request_data: ReqeustGetBookInfo, db: Session):
    requested_book = get_item(BookInfo, request_data.bookinfo_id, db)

    if not requested_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Requested book not found")

    response = BookInfoResponse(
        bookinfo_id=requested_book.id,
        book_title=requested_book.book_title,
        code=requested_book.code,
        category_name=requested_book.category_name,
        subtitle=requested_book.subtitle,
        author=requested_book.author,
        publisher=requested_book.publisher,
        publication_year=requested_book.publication_year,
        image_url=requested_book.image_url,
        version=requested_book.version,
        major=requested_book.major,
        language=requested_book.language
    )
    return response
