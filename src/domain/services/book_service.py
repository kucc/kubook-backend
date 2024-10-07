from fastapi import HTTPException, status
from sqlalchemy import and_, or_, select
from sqlalchemy.orm import Session, joinedload

from domain.schemas.book_schemas import DomainResGetBookItem
from repositories.models import Book, BookInfo


async def service_search_books(searching_keyword: str, db: Session):
    keyword = f"%{searching_keyword}%"

    stmt = (
        select(Book)
        .join(BookInfo)
        .options(joinedload(Book.book_info).load_only(BookInfo.book_title, BookInfo.category_name, BookInfo.image_url))
        .where(
            and_(
                Book.is_deleted == False,
                or_(
                    BookInfo.book_title.ilike(keyword),
                    BookInfo.author.ilike(keyword),
                    BookInfo.publisher.ilike(keyword),
                ),
            )
        )
        # .order_by(BookInfo.updated_at)
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
        DomainResGetBookItem(
            book_id=book.id,
            book_info_id=book.book_info_id,
            book_title=book.book_info.book_title,
            category_name=book.book_info.category_name,
            image_url=book.book_info.image_url,
            book_status=book.book_status,
            created_at=book.created_at,
            updated_at=book.updated_at,
        )
        for book in books
    ]

    return response
