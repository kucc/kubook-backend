from datetime import date

from fastapi import HTTPException, status
from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from domain.schemas.bookrequest_schemas import (
    DomainReqDelBookRequest,
    DomainReqGetBookRequest,
    DomainReqPutBookRequest,
    DomainResBookRequest,
)
from repositories.models import RequestedBook
from utils.crud_utils import get_item


async def service_update_bookrequest(request_data: DomainReqPutBookRequest, db: Session):
    requested_book = get_item(RequestedBook, request_data.request_id, db)
    if requested_book.user_id != request_data.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Deny permission to update this book request")

    request_book = requested_book.__dict__
    updated_book = request_data.__dict__
    try:
        for key, value in updated_book.items():
            if value is not None and key in request_book:
                if isinstance(value, type(request_book[key])):
                    setattr(requested_book, key, value)
                else:
                    raise HTTPException(
                        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                        detail=f"Invalid value type for column {key}. Expected {type(request_book[key])}, got {type(value)}.",
                    )
        db.add(requested_book)
        db.flush()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error occurred during update: {str(e)}",
        ) from e
    else:
        db.commit()
        db.refresh(requested_book)
        # domain response schema 생성
        response = DomainResBookRequest(
            user_id=requested_book.user_id,
            request_id=requested_book.id,
            book_title=requested_book.book_title,
            publication_year=requested_book.publication_year,
            request_link=requested_book.request_link,
            reason=requested_book.reason,
            processing_status=requested_book.processing_status,
            request_date=requested_book.requested_at.date(),
            reject_reason=requested_book.reject_reason,
        )
        return response


async def service_read_bookrequest(request_data: DomainReqGetBookRequest, db: Session) -> list[DomainResBookRequest]:
    stmt = (
        select(RequestedBook)
        .where(and_(RequestedBook.user_id == request_data.user_id, RequestedBook.is_deleted == False))
        .order_by(RequestedBook.updated_at)
    )
    try:
        requested_book_list = db.scalars(stmt).all()
        if not requested_book_list:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Requested book not found")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error occurred during retrieve: {str(e)}",
        ) from e
    response = [
        DomainResBookRequest(
            request_id=book.id,
            user_id=book.user_id,
            book_title=book.book_title,
            publication_year=book.publication_year,
            request_link=book.request_link,
            reason=book.reason,
            processing_status=book.processing_status,
            request_date=book.requested_at.date(),
            reject_reason=book.reject_reason,
        )
        for book in requested_book_list
    ]
    return response


async def service_delete_bookrequest(request_data: DomainReqDelBookRequest, db: Session):
    requested_book = get_item(RequestedBook, request_data.request_id, db)
    if requested_book.user_id != request_data.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Deny permission to update this book request")
    try:
        requested_book.processing_status = 2
        requested_book.processed_date = date.today()
        requested_book.is_deleted = True
        db.add(requested_book)
        db.flush()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error occurred during update: {str(e)}",
        ) from e
    else:
        db.commit()
        db.refresh(requested_book)
        return
