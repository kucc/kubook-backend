

from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from domain.enums.status import BookRequestStatus
from domain.schemas.bookrequest_schemas import (
    DomainReqAdminPutBookRequest,
    DomainResAdminGetBookRequest,
    DomainResBookRequest,
)
from repositories.models import RequestedBook


async def service_admin_read_bookrequest(db: Session, page: int, limit: int):
    offset = (page-1)*limit
    stmt = (select(RequestedBook).where(RequestedBook.is_deleted==False).order_by(RequestedBook.updated_at.desc())
                  .limit(limit).offset(offset))
    bookrequest = db.execute(stmt).scalars().all()
    total_count = db.execute(select(func.count()).select_from(RequestedBook)
                             .where(RequestedBook.is_deleted==False)).scalar()
    if offset>=total_count:
      raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Page is out of range"
      )
    if not bookrequest:
      raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Not found"
      )
    result = [DomainResBookRequest(
      user_id=book.user_id,
      request_id=book.id,
      book_title=book.book_title,
      publication_year=book.publication_year,
      request_link=book.request_link,
      reason=book.reason,
      processing_status=book.processing_status,
      request_date=book.request_date,
      reject_reason=book.reject_reason
    ) for book in bookrequest]

    response = DomainResAdminGetBookRequest(
      data=result,
      count=total_count
    )
    return response


async def service_admin_update_bookrequest(db:Session, request: DomainReqAdminPutBookRequest):
    stmt = select(RequestedBook).where(RequestedBook.id==request.request_id)
    request_book = db.execute(stmt).scalar_one_or_none()
    if not request_book:
      raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Not found"
      )
    if request.processing_status not in {processing_status.name for processing_status in BookRequestStatus}:
      raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid processing status"
      )
    if request.processing_status == BookRequestStatus.REJECTED and request.reject_reason is None:
      raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Reject reason is missed"
      )

    try:
      request_book.processing_status = request.processing_status
      request_book.reject_reason = request.reject_reason
      request_book.updated_at = datetime.now()

      db.flush()

    except IntegrityError as e:
      db.rollback()
      raise HTTPException(
          status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
          detail=f"Integrity Error occurred during update the Review item.: {str(e)}",
      ) from e

    except Exception as e:
      db.rollback()
      raise HTTPException(
          status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
          detail=f"Unexpected error occurred during update: {str(e)}",
      ) from e

    else:
      db.commit()
      db.refresh(request_book)
      result = DomainResBookRequest(
        user_id=request_book.user_id,
        request_id=request_book.id,
        book_title=request_book.book_title,
        publication_year=request_book.publication_year,
        request_link=request_book.request_link,
        reason=request_book.reason,
        processing_status=request_book.processing_status,
        request_date=request_book.request_date,
        reject_reason=request_book.reject_reason
      )
      return result
