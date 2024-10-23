from fastapi import HTTPException, status
from sqlalchemy import and_, select
from sqlalchemy.orm import Session, selectinload

from repositories.models import Loan
from routes.admin.response.loan_response import AdminBaseLoan, GetAdminLoanList, RouteResGetAdminLoanList


async def service_admin_read_loans(db: Session):
    """
        DB loan 테이블에 존재하지 않는 user, book이 있으면 오류 발생함.
    """
    stmt_current = (
        select(Loan)
        .options(selectinload(Loan.user), selectinload(Loan.book))
        .where(
            and_(
                Loan.return_status == False,
                Loan.is_deleted == False
            )
        )
        .order_by(Loan.updated_at)
    )

    stmt_completed = (
        select(Loan)
        .options(selectinload(Loan.user), selectinload(Loan.book))
        .where(
            and_(
                Loan.return_status == True,
                Loan.is_deleted == False
            )
        )
        .order_by(Loan.updated_at)
    )
    try:
        loans_current = db.execute(stmt_current).scalars().all()

        loans_completed = db.execute(stmt_completed).scalars().all()

        if not loans_current and not loans_completed:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Loans not found")

        current_response = [
            AdminBaseLoan(
                book_id=loan.id,
                user_id=loan.user_id,
                user_name=loan.user.user_name,
                code=loan.book.code,
                book_title=loan.book.book_title,
                loan_date=loan.loan_date,
                due_date=loan.due_date,
                extend_status=loan.extend_status,
                created_at=loan.created_at,
                updated_at=loan.updated_at,
            )
            for loan in loans_current
        ]

        completed_response = [
            AdminBaseLoan(
                book_id=loan.id,
                user_id=loan.user_id,
                user_name=loan.user.user_name,
                code=loan.book.code,
                book_title=loan.book.book_title,
                loan_date=loan.loan_date,
                due_date=loan.due_date,
                extend_status=loan.extend_status,
                created_at=loan.created_at,
                updated_at=loan.updated_at,
            )
            for loan in loans_completed
        ]

        response = RouteResGetAdminLoanList(
            current=GetAdminLoanList(
                data=current_response,
                count=len(current_response)
            ),
            completed=GetAdminLoanList(
                data=completed_response,
                count=len(completed_response)
            )
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error occurred during retrieve: {str(e)}",
        ) from e

    return response
