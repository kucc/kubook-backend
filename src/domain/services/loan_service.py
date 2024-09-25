from datetime import datetime as _datetime
from datetime import timedelta
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import Session
from sqlalchemy import select, and_

from domain.schemas.loan_schemas import LoanItem, LoanResponse, LoanCreateRequest, LoanExtendRequest
from repositories.models import Loan, Book


async def get_all_user_loans(user_id, db: Session):
    stmt = select(Loan).where(and_(Loan.user_id == user_id, Loan.is_deleted == False)).order_by(Loan.updated_at)

    try:
        loans = db.scalars(stmt).all()  # loans를 리스트로 반환
        if not loans:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Loans not found")
        result = [
            LoanResponse(
                loan_id=loan.id,
                user_id=loan.user_id,
                book_id=loan.book_id,
                loan_date=loan.loan_date,
                due_date=loan.due_date,
                extend_status=loan.extend_status,
                overdue_days=loan.overdue_days,
                return_status=loan.return_status,
                return_date=loan.return_date
            )
            for loan in loans
        ]
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Unexpected error occurred during retrieve: {str(e)}")
    return result


async def extend_loan(request: LoanExtendRequest, db: Session):
    stmt = select(Loan).where(and_(Loan.id == request.loan_id, Loan.is_deleted == False))

    try:
        loan = db.execute(stmt).scalar_one()

        if loan.user_id != request.user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="You do not have permission to access this loan.")
        # 이미 반납된 도서인지 확인
        if loan.return_status:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="This loan has already been returned.")
        # 이미 연장된 도서인지 확인
        if loan.extend_status:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="This loan has already been extended.")

        loan.due_date = loan.due_date + timedelta(days=7)
        loan.extend_status = True
        loan.updated_at = _datetime.now()

        db.flush()
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Loan not found")
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

        result = LoanItem(
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
            return_date=loan.return_date
        )

        return result


async def create_loan(request: LoanCreateRequest, db: Session):
    stmt = select(Book).where(Book.id == request.book_id)
    valid_book_id = db.execute(stmt).scalar_one_or_none()

    if not valid_book_id:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid book ID"
        )

    loan = Loan(
        book_id=request.book_id,
        user_id=request.user_id,
        loan_date=_datetime.today().date(),
        due_date=(_datetime.today() + timedelta(days=14)).date(),
        created_at=_datetime.now(),
        updated_at=_datetime.now()
    )

    try:
        db.add(loan)
        db.flush()

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Unexpected error occurred: {str(e)}")
    else:
        db.commit()
        db.refresh(loan)

        result = LoanItem(
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
            return_date=loan.return_date
        )
        return result
