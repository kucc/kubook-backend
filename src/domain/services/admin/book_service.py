from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from repositories.models import Book
from routes.admin.response.book_response import RouteAdminGetBookItem, RouteResAdminGetBookList


async def service_admin_read_books(
        book_title: str,
        category_name: str,
        author: str,
        publisher: str,
        return_status: bool,
        db: Session
):
    if book_title is not None and len(book_title) < 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="도서 제목은 최소 2글자 이상이어야 합니다."
        )
    keyword = f"%{book_title}%"

    stmt = (
        select(Book)
        .where(
            Book.is_deleted == False,
        )
    )

    if book_title:
        stmt = stmt.where(Book.book_title.ilike(keyword))
    if category_name:
        stmt = stmt.where(Book.category_name.ilike(f"%{category_name}%"))
    if author:
        stmt = stmt.where(Book.author.ilike(f"%{author}%"))
    if publisher:
        stmt = stmt.where(Book.publisher.ilike(f"%{publisher}%"))
    if return_status is not None:
        stmt = stmt.where(Book.loans.return_status == return_status)

    try:
        books = db.execute(stmt.order_by(Book.updated_at.desc())).scalars().all() # 최신 업데이트 순으로 정렬

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
