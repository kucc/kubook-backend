from fastapi import HTTPException, status
from sqlalchemy import select, text
from sqlalchemy.orm import Session, joinedload

from domain.schemas.admin.loan_schema import DomainAdminGetLoanItem
from repositories.models import Loan


async def service_admin_search_loans(
    user_name: str | None,
    book_title: str | None,
    category_name: str | None,
    return_status: str | None,
    db: Session
) -> list[DomainAdminGetLoanItem]:
    stmt = (
        select(Loan)
        .options(joinedload(Loan.user), joinedload(Loan.book))
        .join(Loan.user)
        .join(Loan.book)
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

        search_loans = [
            DomainAdminGetLoanItem(
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
            for loan in loans
        ]

    except HTTPException as e:
            raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error occurred during retrieve: {str(e)}",
        ) from e

    return search_loans
