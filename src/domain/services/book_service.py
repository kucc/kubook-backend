from math import ceil

from fastapi import HTTPException, status
from sqlalchemy import and_, func, or_, select, text
from sqlalchemy.orm import Session

from domain.schemas.book_schemas import (
    DomainReqGetBook,
    DomainResGetBook,
    DomainResGetBookItem,
    DomainResGetBookList,
)
from repositories.models import Book, Loan


async def service_search_books(
    search: str,
    is_loanable: bool,
    page: int,
    limit: int,
    db: Session
) -> DomainResGetBookList:
    if not search and is_loanable is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Searching keyword or is_loanable should be provided"
        )

    offset = (page - 1) * limit # Calculate offset based on the page numbe

    latest_loan_subq = (
        select(Loan.return_status)
        .where(and_(Loan.book_id == Book.id, Loan.is_deleted == False))
        .order_by(Loan.updated_at.desc())
        .limit(1)
    ).scalar_subquery()

    stmt = (
        select(
            Book.id,
            Book.book_title,
            Book.category_name,
            Book.image_url,
            Book.book_status,
            Book.created_at,
            Book.updated_at,
            latest_loan_subq.label("loan_status")
        )
        .where(and_(Book.is_deleted == False, Book.book_status == True))
    )

    if search: # if search keyword is provided
        search_columns = ['book_title', 'author', 'publisher', 'category_name']

        # Create a list of conditions for OR operation
        conditions = [
            text(f"MATCH({column}) AGAINST(:{column} IN BOOLEAN MODE)")
            for column in search_columns
        ]

        # 모든 조건을 OR로 결합
        stmt = stmt.where(or_(*conditions))

        # 각 열에 대해 검색 키워드 파라미터 설정
        search_params = {column: f"{search}*" for column in search_columns}
        stmt = stmt.params(**search_params)

    if is_loanable is not None: # is_lonable = True or Flase
            if not is_loanable:
                # loan.return_status = False
                stmt = stmt.where(latest_loan_subq == False)
            else:
                # loan.return_status = True or null
                stmt = stmt.where(or_(latest_loan_subq == True, latest_loan_subq.is_(None)))


    # print(stmt) # 디버깅용
    try:
        books = (
            db.execute(
                stmt
                .order_by(Book.updated_at.desc(), Book.id.asc())
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

        # Get total count using the same stmt conditions
        count_stmt = stmt.with_only_columns(func.count())
        total = db.execute(count_stmt).scalar()

        if ceil(total/limit) < page:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Page is out of range"
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

        # loan_status == None이면 True
        loanable = True if loan_status is None else loan_status

        search_books.append(
            DomainResGetBookItem(
                book_id=book_id,
                book_title=book_title,
                category_name=category_name,
                image_url=image_url,
                book_status=book_status,
                created_at=created_at,
                updated_at=updated_at,
                loanable=loanable
            )
        )

    response = DomainResGetBookList(
        data=search_books,
        total=total
    )
    return response


async def service_read_book(request_data: DomainReqGetBook, db: Session):
    stmt = (select(Book).
            where(and_(
                Book.id == request_data.book_id,
                Book.is_deleted == False,
                Book.book_status == True,     # 조건 추가
            )))
    book = db.execute(stmt).scalar_one_or_none()

    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Requested book not found")

    # loanable
    loanable = True

    if book.loans:
        for loan in book.loans:
            if not loan.is_deleted:
                if not loan.return_status:
                    loanable = False
                break

    response = DomainResGetBook(
        book_id=book.id,
        book_title=book.book_title,
        loanable=loanable,
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
    latest_loan_subq = (
        select(Loan.return_status)
        .where(and_(Loan.book_id == Book.id, Loan.is_deleted == False))
        .order_by(Loan.updated_at.desc())
        .limit(1)
    ).scalar_subquery()

    stmt = (
        select(
            Book.id,
            Book.book_title,
            Book.category_name,
            Book.image_url,
            Book.book_status,
            Book.created_at,
            Book.updated_at,
            latest_loan_subq.label("loan_status"),
        )
        .where(and_(Book.is_deleted == False, Book.book_status == True))
    )
    try:
        books = (
            db.execute(
                stmt
                .order_by(Book.updated_at.desc(), Book.id.asc())
                .limit(limit)
                .offset(offset)
            ).all()
        )

        if not books:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Books not found"
            )

        # Get total count using the same stmt conditions
        count_stmt = stmt.with_only_columns(func.count())
        total = db.execute(count_stmt).scalar_one()

        if ceil(total/limit) < page:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Page is out of range"
            )

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error occurred during retrieve: {str(e)}",
        ) from e

    result = []
    for book in books:
        (book_id, book_title, category_name, image_url, book_status, created_at, updated_at, loan_status) = book

        loanable = True if loan_status is None else loan_status

        result.append(
            DomainResGetBookItem(
                book_id=book_id,
                book_title=book_title,
                category_name=category_name,
                image_url=image_url,
                book_status=book_status,
                created_at=created_at,
                updated_at=updated_at,
                loanable=loanable
            )
        )

    response = DomainResGetBookList(
        data=result,
        total=total
    )
    return response
