from fastapi import HTTPException, status
from sqlalchemy import and_, or_, select
from sqlalchemy.orm import Session

from domain.schemas.book_schemas import DomainReqGetBook, DomainResGetBook
from repositories.models import Book
from utils.crud_utils import get_item


async def service_search_books(searching_keyword: str, db: Session):
    keyword = f"%{searching_keyword}%"

    stmt = (
        select(Book)
        .where(
            and_(
                Book.is_deleted == False,
                or_(
                    Book.book_title.ilike(keyword),
                    Book.author.ilike(keyword),
                    Book.publisher.ilike(keyword),
                    Book.category_name.ilike(keyword),
                ),
            )
        )
        .order_by(Book.updated_at)
    )
    try:
        books = db.execute(stmt).scalars().all()

        if not books:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Books not found")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error occurred during retrieve: {str(e)}",
        ) from e

    response = [
        DomainResGetBook(
            book_id=book.id,
            book_title=book.book_title,
            code=book.code,
            category_name=book.category_name,
            subtitle=book.subtitle,
            author=book.author,
            publisher=book.publisher,
            publcation_year=book.publication_year,
            image_url=book.image_url,
            version=book.version,
            major=book.major,
            language=book.language,
            donor_name=book.donor_name,
            book_status=book.book_status,
        )
        for book in books
    ]

    return response


async def service_read_book(request_data: DomainReqGetBook, db: Session):
    book = get_item(Book, request_data.book_id, db)

    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Requested book not found")

    response = DomainResGetBook(
        book_id=book.id,
        book_title=book.book_title,
        code=book.code,
        category_name=book.category_name,
        subtitle=book.subtitle,
        author=book.author,
        publisher=book.publisher,
        publcation_year=book.publication_year,
        image_url=book.image_url,
        version=book.version,
        major=book.major,
        language=book.language,
        donor_name=book.donor_name,
        book_status=book.book_status,
    )
    return response
