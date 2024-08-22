from datetime import timedelta
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy import select

from repositories.loan_repository import Loan
from domain.schemas.loan_schemas import LoanExtendRequest


def get_all_user_loans(user_id, db: Session):
    stmt = select(Loan).filter(Loan.user_id == user_id)

    try:
        loans = db.scalars(stmt).all()
        if loans[0] is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Loans not found")

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Unexpected error occurred during retrieve: {str(e)}")
    return loans


def extend_loan(request: LoanExtendRequest, db: Session):
    stmt = select(Loan).filter(Loan.user_id == request.user_id, Loan.id == request.loan_id)

    try:
        loan = db.scalars(stmt.limit(1)).first()
        if loan is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Loan not found")
        # 이미 반납된 도서인지 확인
        if loan.return_status:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="This loan has already been returned.")

        # 이미 연장된 도서인지 확인
        if loan.extend_status:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="This loan has already been extended.")

        loan.due_date = loan.due_date + timedelta(days=7)

        db.flush()

    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail=f"Integrity Error occurred during update the new Loan item.: {str(e)}")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Unexpected error occurred during update: {str(e)}")
    else:
        db.commit()
        db.refresh(loan)
        return loan
