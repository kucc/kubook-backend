from fastapi import HTTPException, status
from sqlalchemy import or_, select, text
from sqlalchemy.orm import Session

from domain.schemas.book_schemas import DomainReqGetBook, DomainResGetBook, DomainResGetBookList
from repositories.models import Book, Loan
from utils.crud_utils import get_item


async def service_search_books(
    searching_keyword: str,
    page: int,
    limit: int,
    db: Session
) -> DomainResGetBookList:
    offset = (page - 1) * limit # Calculate offset based on the page numbe

    latest_loan_subq = (
        select(Loan.return_status)
        .where(Loan.book_id == Book.id)
        .order_by(Loan.updated_at.desc())
        .limit(1)
    )
    stmt = (
        select(
            Book.id,
            Book.book_title,
            Book.category_name,
            Book.image_url,
            Book.book_status,
            Book.created_at,
            Book.updated_at,
            latest_loan_subq.scalar_subquery().label("loan_status")
        )
        .where(Book.is_deleted == False)
    )

    search_columns = ['book_title', 'author', 'publisher', 'category_name']

    # OR 조건을 위한 조건 리스트 생성
    conditions = [
        text(f"MATCH({column}) AGAINST(:{column} IN BOOLEAN MODE)")
        for column in search_columns
    ]

    # 모든 조건을 OR로 결합
    stmt = stmt.where(or_(*conditions))

    # 각 열에 대해 검색 키워드 파라미터 설정
    search_params = {column: f"{searching_keyword}*" for column in search_columns}
    stmt = stmt.params(**search_params)

    print(stmt)
    try:
        books = (
            db.execute(
                stmt
                .order_by(Book.updated_at.desc())
                .limit(limit)
                .offset(offset)
            )
            .all()
        )

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

    search_books = []
    for book in books:
        (book_id, book_title, category_name, image_url, book_status, created_at, updated_at, loan_status) = book

        search_books.append(
            DomainResGetBookList(
                book_id=book_id,
                book_title=book_title,
                category_name=category_name,
                image_url=image_url,
                book_status=book_status,
                created_at=created_at,
                updated_at=updated_at,
                loan_status=loan_status
            )
        )

    return search_books


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
