from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from domain.enums.book_category import BookCategoryStatus
from domain.schemas.book_schemas import DomainReqAdminPostBook, DomainResAdminPostBook
from repositories.models import Book


async def service_admin_create_book(request: DomainReqAdminPostBook, db: Session):
    # check if the book already exists in database
    stmt = select(Book).where(Book.book_title == request.book_title)
    exist_request = db.execute(stmt).scalar_one_or_none()

    if exist_request:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Already exists")
    if request.code[0] not in {category.name for category in BookCategoryStatus}:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Invalid Category")
    if request.category_name not in {category.category for category in BookCategoryStatus}:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Invalid Category")
    new_book = Book(
        book_title = request.book_title,
        code = request.code,
        category_name = request.category_name,
        subtitle = request.subtitle,
        author = request.author,
        publisher = request.publisher,
        publication_year = request.publication_year,
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
        db.commit()
        db.refresh(new_book)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                             detail=f"Unexpected error occurred: {str(e)}") from e

    domain_res = DomainResAdminPostBook(
        book_id=new_book.id,
        book_title=new_book.book_title,
        code=new_book.code,
        category_name=new_book.category_name,
        subtitle=new_book.subtitle,
        author=new_book.author,
        publisher=new_book.publisher,
        publication_year=new_book.publication_year,
        image_url=new_book.image_url,
        version=new_book.version,
        major=new_book.major,
        language=new_book.language,
        book_status=new_book.book_status,
        donor_name=new_book.donor_name,
        created_at=new_book.created_at,
        updated_at=new_book.updated_at
    )
    return domain_res
