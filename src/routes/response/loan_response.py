from datetime import date, timedelta
from datetime import datetime as _datetime

from pydantic import BaseModel, Field

from domain.schemas.loan_schemas import DomainResGetLoan


class RouteResGetLoanList(BaseModel):
    """
    LoanListResponse 모델은 대출 항목들의 목록과 해당 목록에 포함된 항목 개수를 반환하는 응답 구조입니다.

    Attributes:
        data (List[LoanResponse]): 대출 항목의 목록을 담고 있는 배열입니다.
        count (int): data 배열의 요소 개수를 나타냅니다.
    """
    data: list[DomainResGetLoan]
    count: int = Field(description="data 배열의 요소 개수")


class RouteResPostLoan(BaseModel):
    loan_id: int = Field(title="loan_id", description="대출 정보 id", example=1, gt=0)
    book_id: int = Field(title="book_id", description="대출한 책 ID", example=1, gt=0)
    user_id: int = Field(title="user_id", description="대출한 사용자 ID", example=1, gt=0)
    loan_date: date = Field(title="loan_date", description="대출 날짜", example=_datetime.today().date())
    due_date: date = Field(title="due_date", description="반납 기한", example=(_datetime.today() + timedelta(days=14)).date())
    extend_status: bool = Field(title="extend_status", description="연장 상태", example=True)
    overdue_days: int = Field(title="overdue_days", description="연체 일자", example=1)
    return_status: bool = Field(title="return_status", description="반납 상태", example=False)
    return_date: date | None = Field(title="return_date", description="반납 날짜", example=None)
