from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from domain.schemas.loan_schemas import DomainResGetLoanItem
from repositories.models import Loan
from utils.crud_utils import get_item


async def service_admin_toggle_loan_return(
    loan_id: int,
    db: Session
) -> DomainResGetLoanItem:
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

        result = DomainResGetLoanItem(
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
