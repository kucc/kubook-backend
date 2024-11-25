from fastapi import HTTPException, status
from sqlalchemy import select, text
from sqlalchemy.orm import Session, selectinload

from domain.schemas.admin.book_schema import DomainAdminGetBookItem
from repositories.models import Book


async def service_admin_search_books(
        book_title: str | None,
        category_name: str | None,
        author: str | None,
        publisher: str | None,
        return_status: bool | None,
        db: Session
) -> list[DomainAdminGetBookItem]:
    stmt = (select(Book).options(selectinload(Book.loans)).where(Book.is_deleted == False,))

    if book_title:
        stmt = (
            stmt.where(text("MATCH(book_title) AGAINST(:book_title IN BOOLEAN MODE)"))
                .params(book_title=f"{book_title}*")
        )
    if category_name:
        stmt = (
            stmt.where(text("MATCH(category_name) AGAINST(:category_name IN BOOLEAN MODE)"))
                .params(category_name=f"{category_name}*")
        )
    if author:
        stmt = (
            stmt.where(text("MATCH(author) AGAINST(:author IN BOOLEAN MODE)"))
                .params(author=f"{author}*")
        )
    if publisher:
        stmt = (
            stmt.where(text("MATCH(publisher) AGAINST(:publisher IN BOOLEAN MODE)"))
                .params(publisher=f"{publisher}*")
        )

    try:
        books = db.execute(stmt.order_by(Book.updated_at.desc())).scalars().all() # 최신 업데이트 순으로 정렬

        if not books:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Books not found")

        search_books = []
        for book in books:
            loan_status = None
            if book.loans and len(book.loans) > 0:
                latest_load = max(book.loans, key=lambda loan: loan.updated_at, default=None)
                loan_status = latest_load.return_status if latest_load else None

                if return_status is not None and loan_status != return_status:
                    continue

            search_books.append(
                DomainAdminGetBookItem(
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
                    loan_status=loan_status
                )
            )

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error occurred during retrieve: {str(e)}",
        ) from e

    return search_books
