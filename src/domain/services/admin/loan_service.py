from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from repositories.models import Loan
from routes.admin.response.loan_response import RouteAdminGetLoanItem, RouteResAdminGetLoanList


async def service_admin_search_loans(
    user_name: str | None,
    book_title: str | None,
    category_name: str | None,
    return_status: str | None,
    db: Session
):
    stmt = (
        select(Loan)
        .options(selectinload(Loan.user), selectinload(Loan.book))
        .where(
            Loan.is_deleted == False
        )
    )

    keyword = f"%{book_title}%"

    if user_name:
        stmt = stmt.where(Loan.user.user_name.ilike(f"%{user_name}%"))
    if book_title:
        stmt = stmt.where(Loan.book.book_title.ilike(keyword))
    if category_name:
        stmt = stmt.where(Loan.book.category_name.ilike(f"%{category_name}%"))
    if return_status is not None:
        stmt = stmt.where(Loan.return_status == return_status)

    try:
        loans = db.execute(stmt.order_by(Loan.updated_at.desc())).scalars().all()

        if not loans:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Loans not found")

        search_loans = [
            RouteAdminGetLoanItem(
                book_id=loan.id,
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

        response = RouteResAdminGetLoanList(
            data=search_loans,
            count=len(search_loans)
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error occurred during retrieve: {str(e)}",
        ) from e

    return response
