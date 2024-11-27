

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from repositories.models import RequestedBook
from src.domain.schemas.bookrequest_schemas import DomainResBookRequest


async def service_admin_read_bookreqeust(db: Session):
    stmt = select(RequestedBook).where(RequestedBook.is_deleted==False).order_by(RequestedBook.updated_at.desc())
    bookrequest = db.execute(stmt).scalars().all()

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

    return result
