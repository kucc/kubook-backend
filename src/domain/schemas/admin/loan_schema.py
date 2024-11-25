from datetime import date, datetime, timedelta

from pydantic import BaseModel, Field


class DomainAdminGetLoanItem(BaseModel):
    loan_id: int = Field(title="loan_id", description="대출 id", example=1, gt=0)
    book_id: int = Field(title="book_id", description="대출한 책 ID", example=1, gt=0)
    user_id: int = Field(title="user_id", description="대출한 사용자 ID", example=1, gt=0)
    user_name: str = Field(title="user_name", description="리뷰한 사용자 이름", example="test")
    code: str = Field(title="code", description="책 코드", example="A3")
    book_title: str = Field(title="book_title", description="구매 요청한 책 제목", example="book1")
    loan_date: date = Field(title="loan_date", description="대출 날짜", example=datetime.today().date())
    due_date: date = Field(title="due_date", description="반납 기한", example=(datetime.today() + timedelta(days=14)).date())
    extend_status: bool = Field(title="extend_status", description="연장 상태", example=True)
    return_status: bool = Field(title="return_status", description="반납 상태", example=False)
    return_date: date | None = Field(title="return_date", description="반납 날짜", example=None)
    created_at: datetime = Field(title="create_at", description="생성일시", example=datetime.now())
    updated_at: datetime = Field(title="update_at", description="수정일시", example=datetime.now())
