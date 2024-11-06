from fastapi import HTTPException, status
from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from repositories.models import Book
from routes.admin.response.book_response import RouteAdminGetBookItem, RouteResAdminGetBookList


async def service_admin_read_books(book_title: str, db: Session):
    if len(book_title) < 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="도서 제목은 최소 2글자 이상이어야 합니다."
        )
    keyword = f"%{book_title}%"

    stmt = (
        select(Book)
        .where(
            and_(
                Book.is_deleted == False,
                Book.book_title.ilike(keyword)
            )
        )
        .order_by(Book.updated_at)
    )

    try:
        books = db.execute(stmt).scalars().all()

        if not books:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Books not found")

        search_books = [
            RouteAdminGetBookItem(
                book_id=book.id,
                book_title=book.book_title,
                code=book.code,
                category_name=book.category_name,
                subtitle=book.subtitle,
                author=book.author,
                publisher=book.publisher,
                publication_year=book.publication_year,
                image_url=book.image_url,
                version=book.version,
                major=book.major,
                language=book.language,
                donor_name=book.donor_name,
                book_status=book.book_status,
                created_at=book.created_at,
                updated_at=book.updated_at,
            )
            for book in books
        ]

        response = RouteResAdminGetBookList(
            data=search_books,
            count=len(search_books)
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error occurred during retrieve: {str(e)}",
        ) from e

    return response
