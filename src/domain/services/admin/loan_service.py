# ruff: noqa: C901
from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy import select, text
from sqlalchemy.orm import Session, selectinload

from domain.schemas.loan_schemas import DomainResAdminGetLoan, DomainResGetLoan
from repositories.models import Loan
from utils.crud_utils import calculate_overdue_days, get_item


async def service_admin_toggle_loan_return(
    loan_id: int,
    db: Session
) -> DomainResGetLoan:
    loan = get_item(Loan, loan_id, db)

    try:
        if loan.return_status: # return_stauts가 True이면 False로 변경
            loan.return_status = False
            loan.return_date = None
            # loan.overdue_days = None # 굳이 db에 저장할 필요가 없을 것 같아서 주석 처리
        else: # return_status가 False이면 True로 변경
            loan.return_status = True
            loan.return_date = datetime.now().date()
            loan.overdue_days = calculate_overdue_days(loan.due_date)

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
            overdue_days=calculate_overdue_days(loan.due_date),
            return_status=loan.return_status,
            return_date=loan.return_date,
            book_title=loan.book.book_title,
            code=loan.book.code,
            version=loan.book.version,
        )

    return result

async def service_admin_search_loans(
    user_name: str | None,
    book_title: str | None,
    category_name: str | None,
    return_status: str | None,
    db: Session
) -> list[DomainResAdminGetLoan]:
    stmt = (
        select(Loan)
        .join(Loan.book)
        .join(Loan.user)
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
            stmt.where(text("MATCH(book.category_name) AGAINST(:category_name IN BOOLEAN MODE)"))
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
                DomainResAdminGetLoan(
                    loan_id=loan.id,
                    book_id=loan.book_id,
                    user_id=loan.user_id,
                    user_name=loan.user.user_name,
                    code=loan.book.code,
                    book_title=loan.book.book_title,
                    category_name=loan.book.category_name,
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


async def service_admin_read_loans(db: Session) -> list[DomainResAdminGetLoan]:
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
                DomainResAdminGetLoan(
                    loan_id=loan.id,
                    book_id=loan.book_id,
                    user_id=loan.user_id,
                    user_name=loan.user.user_name,
                    code=loan.book.code,
                    book_title=loan.book.book_title,
                    category_name=loan.book.category_name,
                    loan_date=loan.loan_date,
                    due_date=loan.due_date,
                    overdue_days=calculate_overdue_days(loan.due_date),
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

