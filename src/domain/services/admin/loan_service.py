# ruff: noqa: C901
from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy import select, text
from sqlalchemy.orm import Session, selectinload

from domain.schemas.loan_schemas import DomainAdminGetLoan, DomainResGetLoan
from repositories.models import Loan
from utils.crud_utils import get_item


async def service_admin_toggle_loan_return(
    loan_id: int,
    db: Session
) -> DomainResGetLoan:
    loan = get_item(Loan, loan_id, db)

    try:
        if loan.return_status: # 반납 상태가 True이면 False로 변경
            loan.return_status = False
            loan.return_date = None
        else: # 반납 상태가 False이면 True로 변경
            loan.return_status = True
            loan.return_date = datetime.now().date()

        db.flush()
    except HTTPException as e:
        raise e from e
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error occurred during update: {str(e)}",
        ) from e

    else:
        db.commit()
        db.refresh(loan)

        result = DomainResGetLoan(
            loan_id=loan.id,
            book_id=loan.book_id,
            user_id=loan.user_id,
            created_at=loan.created_at,
            updated_at=loan.updated_at,
            loan_date=loan.loan_date,
            due_date=loan.due_date,
            extend_status=loan.extend_status,
            overdue_days=loan.overdue_days,
            return_status=loan.return_status,
            return_date=loan.return_date,
        )

    return result

async def service_admin_search_loans(
    user_name: str | None,
    book_title: str | None,
    category_name: str | None,
    return_status: str | None,
    db: Session
) -> list[DomainAdminGetLoan]:
    stmt = (
        select(Loan)
        .options(
            selectinload(Loan.user),
            selectinload(Loan.book)
        )
        .where(
            Loan.is_deleted == False
        )
    )

    if book_title:
        stmt = (
            stmt.where(text("MATCH(book.book_title) AGAINST(:book_title IN BOOLEAN MODE)"))
                .params(book_title=f"{book_title}*")
        )
    if user_name:
        stmt = (
            stmt.where(text("MATCH(user.user_name) AGAINST(:user_name IN BOOLEAN MODE)"))
                .params(user_name=f"{user_name}*")
        )
    if category_name:
        stmt = (
            stmt.where(text("MATCH(category_name) AGAINST(:category_name IN BOOLEAN MODE)"))
                .params(category_name=f"{category_name}*")
        )
    if return_status is not None:
        stmt = stmt.where(Loan.return_status == return_status)

    try:
        loans = db.execute(stmt.order_by(Loan.updated_at.desc())).scalars().all()

        if not loans:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Loans not found")

        search_loans = []
        for loan in loans:
            if not loan.user:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"User with ID {loan.user_id} not found for loan ID {loan.id}"
                )
            if not loan.book:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Book with ID {loan.book_id} not found for loan ID {loan.id}"
                )
            search_loans.append(
                DomainAdminGetLoan(
                    loan_id=loan.id,
                    book_id=loan.book_id,
                    user_id=loan.user_id,
                    user_name=loan.user.user_name,
                    code=loan.book.code,
                    book_title=loan.book.book_title,
                    loan_date=loan.loan_date,
                    due_date=loan.due_date,
                    extend_status=loan.extend_status,
                    return_status=loan.return_status,
                    return_date=loan.return_date,
                    created_at=loan.created_at,
                    updated_at=loan.updated_at,
                )
            )

    except HTTPException as e:
            raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error occurred during retrieve: {str(e)}",
        ) from e

    return search_loans


async def service_admin_read_loans(db: Session) -> list[DomainAdminGetLoan]:
    stmt = (
        select(Loan)
        .options(
            selectinload(Loan.user),
            selectinload(Loan.book)
        )
        .where(
            Loan.is_deleted == False
        )
    )

    try:
        loans = db.execute(stmt.order_by(Loan.updated_at.desc())).scalars().all()

        if not loans:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Books not found")

        search_loans = []
        for loan in loans:
            if not loan.user:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"User with ID {loan.user_id} not found for loan ID {loan.id}"
                )
            if not loan.book:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Book with ID {loan.book_id} not found for loan ID {loan.id}"
                )
            search_loans.append(
                DomainAdminGetLoan(
                    loan_id=loan.id,
                    book_id=loan.book_id,
                    user_id=loan.user_id,
                    user_name=loan.user.user_name,
                    code=loan.book.code,
                    book_title=loan.book.book_title,
                    loan_date=loan.loan_date,
                    due_date=loan.due_date,
                    extend_status=loan.extend_status,
                    return_status=loan.return_status,
                    return_date=loan.return_date,
                    created_at=loan.created_at,
                    updated_at=loan.updated_at,
                )
            )

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error occurred during retrieve: {str(e)}",
        ) from e

    return search_loans

