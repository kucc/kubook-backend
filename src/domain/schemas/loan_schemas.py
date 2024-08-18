from datetime import date
from datetime import datetime as _datetime
from datetime import timedelta
from typing import Optional, List

from pydantic import Field, BaseModel


class LoanBase(BaseModel):
    book_id: int = Field(..., title="book_id", description="대출한 책 ID", example=1, ge=0)
    user_id: int = Field(..., title="user_id", description="대출한 사용자 ID", example=1, ge=0)


class LoanInfo(LoanBase):
    loan_date: date = Field(..., title="loan_date", description="대출 날짜", example=_datetime.today().date())
    due_date: date = Field(..., title="due_date", description="반납 기한", example=(_datetime.today() + timedelta(days=14)).date())
    extend_status: bool = Field(False, title="extend_status", description="연장 상태", example=True)
    overdue_days: int = Field(0, title="overdue_days", description="연체 일자", example=1, )
    return_status: bool = Field(False, title="return_status", description="반납 상태", example=False, )
    return_date: Optional[date] = Field(None, title="return_date", description="반납 날짜", example=None)


class Loan(LoanInfo):
    id: int = Field(..., title="loan_id", description="대출 정보 id", example=1, ge=0)
    created_at: _datetime = Field(..., title="create_at", description="생성일시", example=_datetime.now())
    updated_at: _datetime = Field(..., title="update_at", description="수정일시", example=_datetime.now())


class LoanCreate(LoanBase):
    pass


class LoanUpdate(LoanInfo.all_optional("LoanUpdate")):
    pass


class LoanListItem(BaseModel):
    id: int
    user_id: int
    book_id: int
    loan_date: date
    due_date: date
    extend_status: bool
    overdue_days: int
    return_status: bool
    return_date: Optional[date]


class LoanListResponse(BaseModel):
    data: List[LoanListItem] = Field(..., title="loan_list", description="대출 정보 리스트")


class LoanExtendResponse(BaseModel):
    id: int
    due_date: date
    extend_status: bool
