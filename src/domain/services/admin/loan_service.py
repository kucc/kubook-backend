from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from domain.schemas.loan_schemas import DomianResGetLoanItem
from repositories.models import Loan
from utils.crud_utils import get_item


async def service_admin_return_loan(loan_id, db: Session):
    loan = get_item(Loan, loan_id, db)

    # 이미 반납된 도서인지 확인
    if loan.return_status:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This loan has already been returned.")

    try:
        loan.return_status = True

        db.flush()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error occurred during update: {str(e)}",
        ) from e

    else:
        db.commit()
        db.refresh(loan)

        result = DomianResGetLoanItem(
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

async def service_admin_unreturn_loan(loan_id, db: Session):
    loan = get_item(Loan, loan_id, db)

    # 이미 반납되지 않은 도서인지 확인
    if not loan.return_status:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This loan has not been returned yet.")

    try:
        loan.return_status = False

        db.flush()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error occurred during update: {str(e)}",
        ) from e

    else:
        db.commit()
        db.refresh(loan)

        result = DomianResGetLoanItem(
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
