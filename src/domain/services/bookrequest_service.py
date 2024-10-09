
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from domain.schemas.bookrequest_schemas import (BookRequestResponse,
                                                DeleteBookRequestRequest,
                                                ReqeustGetMyBookRequest,
                                                UpdateBookRequestRequest)
from repositories.models import RequestedBook
from utils.crud_utils import get_item, get_item_by_column, update_item


async def update_bookrequest(request_data: UpdateBookRequestRequest, db: Session):
    requested_book = get_item(RequestedBook, request_data.request_id, db)

    if not requested_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Requested book not found"
            ) from None

    # 도서 구매 요청 table 수정
    updated_book = update_item(RequestedBook, request_data.request_id, request_data, db)

    # domain response schema 생성
    response = BookRequestResponse(
        user_id=updated_book.user_id,
        request_id=updated_book.id,
        book_title=updated_book.book_title,
        publication_year=updated_book.publication_year,
        request_link=updated_book.request_link,
        reason=updated_book.reason,
        processing_status=updated_book.processing_status,
        request_date=updated_book.requested_at.date(),
        reject_reason=updated_book.reject_reason
    )
    return response


async def read_bookrequest(request_data: ReqeustGetMyBookRequest, db: Session) -> list[BookRequestResponse]:
    requested_book_list: list[RequestedBook] = get_item_by_column(
        model=RequestedBook,
        columns={'user_id': request_data.user_id},
        db=db
    )

    response = []
    for book in requested_book_list:
        requested_book = BookRequestResponse(
            request_id=book.id,
            user_id=book.user_id,
            book_title=book.book_title,
            publication_year=book.publication_year,
            request_link=book.request_link,
            reason=book.reason,
            processing_status=book.processing_status,
            request_date=book.requested_at.date(),
            reject_reason=book.reject_reason
        )
        response.append(requested_book)
    return response


async def delete_bookrequest(request_data: DeleteBookRequestRequest, db: Session):
    requested_book = get_item(RequestedBook, request_data.request_id, db)

    if not requested_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Requested book not found")

    # 도서 구매 요청 table 수정
    # updated_book = update_item(RequestedBook, request_data.request_id, request_data, db)

    return
