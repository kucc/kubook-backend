
from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy import and_, func, select
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
    total = db.execute(select(func.count()).select_from(RequestedBook)
                             .where(RequestedBook.is_deleted==False)).scalar()
    if offset>=total:
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
      total = total
    )
    return response


async def service_admin_update_bookrequest(db:Session, request: DomainReqAdminPutBookRequest):
    stmt = select(RequestedBook).where(and_(RequestedBook.id==request.request_id, RequestedBook.is_deleted==False))
    request_book = db.execute(stmt).scalar_one_or_none()
    if not request_book:
      raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="BookRequest Not found"
      )
    if not BookRequestStatus.is_valid_enum_value(request.processing_status):
      raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid processing status"
      )

    try:
      request_book.processing_status = request.processing_status
      if request_book.processing_status == BookRequestStatus.REJECTED():
        request_book.reject_reason = request.reject_reason
      else:
        request_book.reject_reason = None
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

async def service_admin_delete_bookrequest(request_id: int, db: Session):
    stmt = select(RequestedBook).where(RequestedBook.id==request_id, RequestedBook.is_deleted==False)
    request_book = db.execute(stmt).scalar_one_or_none()
    if not request_book:
      raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="BookRequest Not found"
      )
    try:
      request_book.is_deleted = True
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
    return
