

from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from domain.enums.status import BookRequestStatus
from domain.schemas.bookrequest_schemas import (
    DomainReqAdminPutBookRequest,
    DomainResAdminGetBookRequest,
    DomainResBookRequest,
)
from repositories.models import RequestedBook


async def service_admin_read_bookreqeust(db: Session, page: int, limit: int):
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
