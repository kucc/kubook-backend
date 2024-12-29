from datetime import datetime

from pydantic import BaseModel, Field


class RouteReqAdminPostSetting(BaseModel):
    start_date: datetime = Field(title="start_date", description="대여 시작일", examples=["2024-12-10"])
    end_date: datetime = Field(title="end_date", description="대여 종료일", examples=["2024-12-25"])
    extend_max_count: int = Field(title="extend_max_count", description="연장 가능 횟수", ge=1, examples=[1, 2, 3])
    extend_days: int = Field(title="extend_days", 
                             description="1회 연장 시 늘어나는 대출 기간", ge=1, examples=[1, 2, 3])
    loan_days: int = Field(title="loan_days", description="대출 1회당 대출 기간", ge=1, examples=[1, 2, 3])
    loan_max_book: int = Field(title="loan_max_book", description="1회당 최대 대출 권수", ge=1, examples=[1, 2, 3])
    request_max_count: int = Field(title="request_max_count", 
                                   description="도서 구매 신청 가능 권수", ge=1, examples=[1, 2, 3])
    request_max_price: int = Field(title="request_max_price", 
                                   description="도서 구매 신청 최대 금액", ge=0, examples=[0, 10000, 20000])

class RouteReqAdminPutSetting(BaseModel):
    start_date: datetime = Field(title="start_date", description="대여 시작일", examples=["2024-12-10"])
    end_date: datetime = Field(title="end_date", description="대여 종료일", examples=["2024-12-25"])
    extend_max_count: int = Field(title="extend_max_count", description="연장 가능 횟수", ge=1, examples=[1, 2, 3])
    extend_days: int = Field(title="extend_days", 
                             description="1회 연장 시 늘어나는 대출 기간", ge=1, examples=[1, 2, 3])
    loan_days: int = Field(title="loan_days", description="대출 1회당 대출 기간", ge=1, examples=[1, 2, 3])
    loan_max_book: int = Field(title="loan_max_book", description="1회당 최대 대출 권수", ge=1, examples=[1, 2, 3])
    request_max_count: int = Field(title="request_max_count",
                                   description="도서 구매 신청 가능 권수", ge=1, examples=[1, 2, 3])
    request_max_price: int = Field(title="request_max_price",
                                   description="도서 구매 신청 최대 금액", ge=0, examples=[0, 10000, 20000])
