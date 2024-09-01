from datetime import date
from datetime import datetime as _datetime
from typing import Optional
from pydantic import Field, BaseModel


class BookRequestRequest(BaseModel):
    user_id: int = Field(title="user_id", description="도서 구매를 요청한 사용자 ID", example=1, ge=0)
    request_id: int = Field(title="book_request_id", description="도서 구매 요청 정보 id", example=1, ge=0)
    book_title: str = Field(title="book_title", description="책 제목", example="FastAPI Tutorial")
    publication_year: int = Field(title="publication_year", description="출판년도", example=2022, gt=0)
    request_link: str = Field(title="request_link", description="요청 링크", example="https://example.com/request")
    reason: str = Field(title="reason", description="이유", example="Need for study")


class BookRequestResponse(BaseModel):
    user_id: int = Field(title="user_id", description="도서 구매를 요청한 사용자 ID", example=1, ge=0)
    request_id: int = Field(title="book_request_id", description="도서 구매 요청 정보 id", example=1, ge=0)
    book_title: str = Field(title="book_title", description="책 제목", example="FastAPI Tutorial")
    publication_year: int = Field(title="publication_year", description="출판년도", example=2022, gt=0)
    request_link: str = Field(title="request_link", description="요청 링크", example="https://example.com/request")
    reason: str = Field(title="reason", description="이유", example="Need for study")
    processing_status: int = Field(0, title="processing_status", description="처리 상태", example=0, ge=0, le=3)
    request_date: date = Field(title="request_date", description="요청 일자", example=_datetime.now().date())
    reject_reason: Optional[str] = Field(None, title="reject_reason", description="거절 사유", example="Not available")
