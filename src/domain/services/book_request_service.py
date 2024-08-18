from typing import Any, Dict

from fastapi import HTTPException, status
from sqlalchemy import delete, select, update
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import Session

from domain.schemas.book_request_schemas import BookRequestUpdateRequest
from domain.schemas.book_request_schemas import BookRequestUpdateResponse
from repositories.requested_book import RequestedBook
from repositories.user_repository import User
from domain.services.user_service import update_item, get_item


async def update(user_id, request_id, request_data, db):
    requested_book = db.query(RequestedBook).filter(RequestedBook.id == request_id).first()

    if not requested_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Requested book not found")

    # 도서 구매 요청 table 수정
    update_item(RequestedBook, request_id, request_data, db)
    # 요청한 user table 수정
    update_item(User, user_id, request_data, db)

    updated_book = get_item(RequestedBook, request_id, db)

    # domain response schema 생성
    response = BookRequestUpdateResponse(
        user_id=updated_book.user_id,
        book_title=updated_book.book_title,
        publication_year=updated_book.publication_year,
        request_link=updated_book.request_link,
        reason=updated_book.reason,
        processing_status=updated_book.processing_status,
        request_date=updated_book.request_date,
        reject_reason=updated_book.reject_reason
    )

    return response
