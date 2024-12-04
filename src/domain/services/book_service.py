from fastapi import HTTPException, status
from sqlalchemy import select, text
from sqlalchemy.orm import Session

from domain.schemas.book_schemas import DomainReqGetBook, DomainResGetBook, DomainResGetBookList
from repositories.models import Book
from utils.crud_utils import get_item


async def service_search_books(
    searching_keyword: str,
    page: int,
    limit: int,
    db: Session
) -> DomainResGetBookList:
    offset = (page - 1) * limit # Calculate offset based on the page numbe

    stmt = (
        select(Book)
        .where(Book.is_deleted == False)
    )

    search_columns = ['book_title', 'author', 'publisher', 'category_name']
    search_conditions = []
    params = {}

    for column in search_columns:
        search_conditions.append(f"MATCH({column}) AGAINST(:{column} IN BOOLEAN MODE)")
        params[column] = f"{searching_keyword}*"

    # Combine all search conditions with OR
    combined_search = text(" OR ".join(search_conditions))
    stmt = stmt.where(combined_search).params(**params)
    """.order_by(Book.updated_at.desc())
        .limit(limit)
        .offset(offset)"""

    try:
        books = (db.execute(
            stmt
            .order_by(Book.updated_at.desc())
            .limit(limit)
            .offset(offset)
        )
        .scalars()
        .all())

        if not books:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Books not found"
            )
    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error occurred during retrieve: {str(e)}",
        ) from e

    response = [
        DomainResGetBookList(
            book_id=book.id,
            book_title=book.book_title,
            category_name=book.category_name,
            image_url=book.image_url,
            book_status=book.book_status,
            created_at=book.created_at,
            updated_at=book.updated_at
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
        publication_year=book.publication_year,
        image_url=book.image_url,
        version=book.version,
        major=book.major,
        language=book.language,
        donor_name=book.donor_name,
        book_status=book.book_status,
        created_at=book.created_at,
        updated_at=book.updated_at
    )
    return response

async def service_read_books(page: int, limit: int, db: Session):
    offset = (page - 1) * limit # Calculate offset based on the page number

    stmt = (
        select(Book)
        .where(
            Book.is_deleted == False
        )
        .order_by(Book.updated_at.desc())
        .limit(limit)
        .offset(offset)
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
            detail=f"Unexpected error occurred during retrieve: {str(e)}",
        ) from e

    response = [
        DomainResGetBookList(
            book_id=book.id,
            book_title=book.book_title,
            category_name=book.category_name,
            image_url=book.image_url,
            book_status=book.book_status,
            created_at=book.created_at,
            updated_at=book.updated_at
        )
        for book in books
    ]

    return response
