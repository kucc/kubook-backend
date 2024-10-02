from fastapi import HTTPException, status
from sqlalchemy import and_, or_, select
from sqlalchemy.orm import Session, selectinload

from domain.schemas.book_schemas import DomainResGetBookItem
from repositories.models import Book, BookInfo


async def service_search_books(searching_keyword: str, db: Session):
    stmt = (
        select(BookInfo)
        .where(
            or_(
                BookInfo.book_title.ilike(searching_keyword),
                BookInfo.author.ilike(searching_keyword),
                BookInfo.publisher.ilike(searching_keyword)
            )
        )
        #.order_by(BookInfo.updated_at)
    )
    try:
        bookinfos = db.execute(stmt).scalars().all()

        if not bookinfos:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Books not found"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error occurred during retrieve: {str(e)}"
            ) from e

    bookinfo_ids = [bookinfo.id for bookinfo in bookinfos]

    stmt = (
        select(Book)
        .options(selectinload(Book.book_info))
        .where(
            and_(
                Book.book_info_id.in_(bookinfo_ids),
                Book.is_deleted == False
            )
        )
    )

    try:
        books = db.execute(stmt).scalars().all()

        if not books:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Books not found"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error occurred during retrieve: {str(e)}"
            ) from e

    response = [
            DomainResGetBookItem(
                book_id=book.id,
                book_info_id=book.book_info_id,
                book_title=book.book_info.book_title,
                category_name=book.book_info.category_name,
                book_status=book.book_status,
                created_at=book.created_at,
                updated_at=book.updated_at
            )
            for book in books
        ]

    return response
