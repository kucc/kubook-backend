from fastapi import HTTPException, status
from sqlalchemy import and_, select
from sqlalchemy.orm import Session, selectinload

from repositories.models import Loan
from routes.admin.response.loan_response import RouteAdminGetLoanItem, RouteResAdminGetLoanList


async def service_admin_read_loans(db: Session):
    stmt = (
        select(Loan)
        .options(selectinload(Loan.user), selectinload(Loan.book))
        .where(
            and_(
                Loan.is_deleted == False
            )
        )
        .order_by(Loan.updated_at)
    )

    try:
        loans = db.execute(stmt).scalars().all()

        if not loans:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Loans not found")

        response = [
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
            data=response,
            count=len(response)
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error occurred during retrieve: {str(e)}",
        ) from e

    return response
