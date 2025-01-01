# ruff: noqa: C901
from datetime import datetime
from math import ceil

from fastapi import HTTPException, status
from sqlalchemy import and_, func, or_, select, text
from sqlalchemy.orm import Session, selectinload

from domain.enums.book_category import BookCategoryStatus
from domain.schemas.book_schemas import (
    DomainAdminGetBookItem,
    DomainAdminGetBookList,
    DomainReqAdminDelBook,
    DomainReqAdminPostBook,
    DomainReqAdminPutBook,
    DomainResAdminPostBook,
    DomainResAdminPutBook,
)
from repositories.models import Book, Loan
from utils.crud_utils import delete_item


async def service_admin_search_books(
    book_title: str | None,
    category_name: str | None,
    author: str | None,
    publisher: str | None,
    is_loanable: bool | None,
    page: int,
    limit: int,
    db: Session
) -> DomainAdminGetBookList:
    offset = (page - 1) * limit # Calculate offset based on the page number

    latest_loan_subq = (
        select(Loan.return_status)
        .where(and_(Loan.book_id == Book.id, Loan.is_deleted == False))
        .order_by(Loan.updated_at.desc())
        .limit(1)
    ).scalar_subquery()

    stmt = (
        select(
            Book,
            latest_loan_subq.label("loan_status")
        )
        .where(Book.is_deleted == False)
    )

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
    if is_loanable is not None: # is_lonable = True or Flase
            if not is_loanable:
                # loan.return_status = False
                stmt = stmt.where(latest_loan_subq == False)
            else:
                # loan.return_status = True or null
                stmt = stmt.where(or_(latest_loan_subq == True, latest_loan_subq.is_(None)))

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

        # Get total count using the same stmt conditions
        count_stmt = stmt.with_only_columns(func.count())
        total = db.execute(count_stmt).scalar_one()

        if not books:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Books not found"
            )

        if ceil(total/limit) < page:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Page is out of range"
            )

        result = []
        for book in books:
            loanable = True if book.loan_status is None else book.loan_status
            book_obj = book.Book  # Get the Book object from the result tuple

            result.append(
                DomainAdminGetBookItem(
                    book_id=book_obj.id,
                    book_title=book_obj.book_title,
                    code=book_obj.code,
                    category_name=book_obj.category_name,
                    subtitle=book_obj.subtitle,
                    author=book_obj.author,
                    publisher=book_obj.publisher,
                    publication_year=book_obj.publication_year,
                    image_url=book_obj.image_url,
                    version=book_obj.version,
                    major=book_obj.major,
                    language=book_obj.language,
                    donor_name=book_obj.donor_name,
                    book_status=book_obj.book_status,
                    created_at=book_obj.created_at,
                    updated_at=book_obj.updated_at,
                    loanable=loanable,
                )
            )

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error occurred during retrieve: {str(e)}",
        ) from e

    response = DomainAdminGetBookList(
        data=result,
        total=total,
    )

    return response


async def service_admin_create_book(request: DomainReqAdminPostBook, db: Session):
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
        book_status = request.book_status,
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

async def service_admin_update_book(request: DomainReqAdminPutBook, db: Session):
    stmt = select(Book).where(Book.id == request.book_id)
    request_book = db.execute(stmt).scalar_one_or_none()

    if not request_book:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Requested Book Not Found")
    if request.code[0] not in {category.name for category in BookCategoryStatus}:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Invalid Category")
    if request.category_name not in {category.category for category in BookCategoryStatus}:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Invalid Category")

    requested_book = request_book.__dict__
    updated_book = request.__dict__

    try:
        for key, value in updated_book.items():
            if value is not None and key in requested_book:
                if isinstance(value, type(requested_book[key])):
                    setattr(request_book, key, value)
                else:
                    raise HTTPException(
                        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                        detail=f"Invalid value type for column {key}. \
                        Expected {type(request_book[key])}, got {type(value)}."
                    )
        request_book.updated_at = datetime.now()
        db.add(request_book)
        db.flush()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error occurred during update: {str(e)}",
        ) from e
    else:
        db.commit()
        db.refresh(request_book)

        domain_res = DomainResAdminPutBook(
        book_id=request_book.id,
        book_title=request_book.book_title,
        code=request_book.code,
        category_name=request_book.category_name,
        subtitle=request_book.subtitle,
        author=request_book.author,
        publisher=request_book.publisher,
        publication_year=request_book.publication_year,
        image_url=request_book.image_url,
        version=request_book.version,
        major=request_book.major,
        language=request_book.language,
        book_status=request_book.book_status,
        donor_name=request_book.donor_name,
        created_at=request_book.created_at,
        updated_at=request_book.updated_at
    )

    return domain_res

async def service_admin_delete_book(request: DomainReqAdminDelBook, db: Session):
    delete_item(Book, request.book_id, db)
    return


async def service_admin_read_books(
    page: int,
    limit: int,
    db: Session,
) -> DomainAdminGetBookList:
    offset = (page - 1) * limit # Calculate offset based on the page numbe

    stmt = (
        select(Book)
        .options(
            selectinload(Book.loans)
        )
        .where(Book.is_deleted == False, Book.book_status == True)
    )

    try:
        books = db.execute(
            stmt
            .order_by(Book.updated_at.desc(), Book.id.asc())
            .limit(limit)
            .offset(offset)
        ).scalars().all()

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

        result = []
        for book in books:
            loanable = True
            if book.loans:
                latest_loan = max(book.loans, key=lambda loan: loan.updated_at, default=None)
                loanable = latest_loan.return_status if latest_loan else True

            result.append(
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
                    loanable=loanable
                )
            )

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error occurred during retrieve: {str(e)}",
        ) from e
    response = DomainAdminGetBookList(
        data=result,
        total=total,
    )

    return response
