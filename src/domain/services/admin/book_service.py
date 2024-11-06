from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from domain.schemas.book_schemas import DomainReqAdminPostBook
from repositories.models import Book


async def service_create_book(request: DomainReqAdminPostBook, db: Session):
    # check if the book already exists in database
    stmt = select(Book).where(Book.book_title == request.book_title)
    exist_request = db.execute(stmt).scalar_one_or_none()

    if exist_request:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Already exists")

    new_book = Book(
        book_title = request.book_title,
        code=request.code,
        category_name = request.category_name,
        subtitle=request.subtitle,
        author=request.autor,
        publisher=request.publisher,
        publication_year=request.publication_year,
        image_url = request.image_url,
        version = request.version,
        major = request.major,
        book_status = True,
        donor_name = request.donor_name,
        created_at = datetime.now(),
        updated_at = datetime.now(),
        is_deleted = False
    )

    try:
        db.add(new_book)
        db.flush()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Unexpected error occurred: {str(e)}") from e
    else:
        db.commit()
        db.refresh(new_book)
    return
