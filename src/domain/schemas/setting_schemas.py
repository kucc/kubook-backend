from datetime import datetime

from pydantic import BaseModel, Field


class DomainResAdminSetting(BaseModel):
    setting_id: int = Field(title="setting_id", description="설정 ID", ge=1)
    start_date: datetime = Field(title="start_date", description="대여 시작일", examples=["2024-12-10 00:00:00"])
    end_date: datetime = Field(title="end_date", description="대여 종료일", examples=["2024-12-31 23:59:59"])
    extend_max_count: int = Field(title="extend_max_count", description="연장 가능 횟수", ge=1)
    extend_days: int = Field(title="extend_days", description="1회 연장 시 늘어나는 대출 기간", ge=1)
    loan_days: int = Field(title="loan_days", description="대출 1회당 대출 기간", ge=1)
    loan_max_book: int = Field(title="loan_max_book", description="1회당 최대 대출 권수", ge=1)
    request_max_count: int = Field(title="request_max_count", description="도서 구매 신청 가능 권수", ge=1)
    request_max_price: int = Field(title="request_max_price", description="도서 구매 신청 최대 금액", ge=0)
