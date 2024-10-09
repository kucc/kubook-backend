from datetime import date

from pydantic import BaseModel, Field


class RouteResPostBookRequest(BaseModel):
    request_id: int = Field(title="purchase_id", description="구매 요청 정보 id", example=1, gt=0)
    user_id: int = Field(title="user_id", description="구매 요청한 사용자 id", example=1, gt=0)
    book_title: str = Field(title="book_title", description="구매 요청한 책 제목", example="book1")
    publication_year: int = Field(title="publication_year", description="출판 년도", example=2024, gt=0)
    request_link: str = Field(title="request_link", description="구매 요청 링크", example="https://www.example.com/request")
    request_date: date = Field(title="request_date", description="구매 요청한 날짜",
                               example=date.today())
    reason: str = Field(title="reason", description="구매 요청 이유", example="학습 목적")
    processing_status: int = Field(title="processing_status", description="구매 요청 처리 상태", example=0, ge=0, le=3)

class RouteResBookRequest(BaseModel):
    user_id: int = Field(title="user_id", description="도서 구매를 요청한 사용자 ID", example=1, gt=0)
    request_id: int = Field(title="request_id", description="도서 구매 요청 ID", example=1, gt=0)
    book_title: str = Field(title="book_title", description="책 제목", example="FastAPI Tutorial")
    publication_year: int = Field(0, title="publication_year", description="출판년도", example=2022, gt=0)
    request_link: str = Field(title="request_link", description="요청 링크", example="https://example.com/request")
    reason: str = Field(title="reason", description="이유", example="Need for study")
    processing_status: int = Field(0, title="processing_status", description="처리 상태", example=0, ge=0, le=3)
    request_date: date = Field(title="request_date", description="요청 일자", example=date.today())
    reject_reason: str | None = Field(None, title="reject_reason", description="거절 사유", example="Not available")


class RouteResBookRequestList(BaseModel):
    data: list[RouteResBookRequest]
    count: int = Field(0, title="bookrequest_count", description="data 배열의 요소 개수", ge=0)
