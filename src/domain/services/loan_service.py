from datetime import timedelta
from fastapi import HTTPException
from sqlalchemy.orm import Session

from repositories.loan_repository import Loan


async def get_all_user_loans(current_user, db: Session):
    user_id = current_user.id

    loans = db.query(Loan).filter(Loan.user_id == user_id).all()

    if not loans:
        raise HTTPException(status_code=404, detail="No loans found")

    return loans


async def extend_loan(current_user, loan_id, db: Session):
    user_id = current_user.id
    loan = db.query(Loan).filter(Loan.id == loan_id, Loan.user_id == user_id).first()

    if not loan:
        raise HTTPException(status_code=404, detail="No loan found")

    # 이미 반납된 도서인지 확인
    if loan.return_status == "TRUE":
        raise HTTPException(status_code=400, detail="This loan has already been returned.")

    # 이미 연장된 도서인지 확인
    if loan.extend_status == "TRUE":
        raise HTTPException(status_code=400, detail="This loan has already been extended.")

    loan.due_date = loan.due_date + timedelta(days=7)

    db.commit()
    db.refresh(loan)

    return loan
