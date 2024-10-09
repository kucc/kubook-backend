from pydantic import BaseModel, Field


class RouteReqPostBookRequest(BaseModel):
    user_id: int = Field(title="user_id", description="구매 요청한 사용자 id", example=1, gt=0)
    book_title: str = Field(title="book_title", description="구매 요청한 책 제목", example="book1")
    publication_year: int = Field(title="publication_year", description="출판 년도", example=2024, gt=0)
    request_link: str = Field(title="request_link", description="구매 요청 링크", example="https://www.example.com/request")
    reason: str = Field(title="reason", description="구매 요청 이유", example="학습 목적")

class RouteReqPutBookRequest(BaseModel):
    book_title: str = Field(title="book_title", description="책 제목", example="FastAPI Tutorial")
    publication_year: int = Field(title="publication_year", description="출판년도", example=2022, gt=0)
    request_link: str = Field(title="request_link", description="요청 링크", example="https://example.com/request")
    reason: str = Field(title="reason", description="이유", example="Need for study")

