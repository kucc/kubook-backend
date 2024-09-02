from typing import List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from domain.schemas.book_request_schemas import UpdateBookRequestRequest as update_bookreq_req
from domain.schemas.book_request_schemas import ReadBookRequestRequest as read_bookreq_req
from domain.schemas.book_request_schemas import BookRequestResponse as bookreq_res
from repositories.requested_book import RequestedBook
from utils.user_service import update_item, get_item, get_item_by_column


async def update_bookreq(request_data: update_bookreq_req, db: Session):
    requested_book = get_item(RequestedBook, request_data.request_id, db)

    if not requested_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Requested book not found")

    # 도서 구매 요청 table 수정
    update_item(RequestedBook, request_data.request_id, request_data, db)
    updated_book = get_item(RequestedBook, request_data.request_id, db)

    # domain response schema 생성
    response = bookreq_res(
        user_id=updated_book.user_id,
        request_id=updated_book.request_id,
        book_title=updated_book.book_title,
        publication_year=updated_book.publication_year,
        request_link=updated_book.request_link,
        reason=updated_book.reason,
        processing_status=updated_book.processing_status,
        request_date=updated_book.request_date,
        reject_reason=updated_book.reject_reason
    )
    return response


async def read_bookreq(request_data: read_bookreq_req, db: Session) -> List[bookreq_res]:
    requested_book_list = get_item_by_column(RequestedBook, {'user_id': request_data.user_id}, db)
    response = []
    for book in requested_book_list:
        requested_book = bookreq_res(
            user_id=book.user_id,
            request_id=book.request_id,
            book_title=book.book_title,
            publication_year=book.publication_year,
            request_link=book.request_link,
            reason=book.reason,
            processing_status=book.processing_status,
            request_date=book.request_date,
            reject_reason=book.reject_reason
        )
        response.append(requested_book)
    return response
