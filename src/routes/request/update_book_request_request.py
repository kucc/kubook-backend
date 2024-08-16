from datetime import date
from datetime import datetime as _datetime
from typing import Optional

from pydantic import Field

from pydantic import BaseModel, Field


class UpdateBookRequest(BaseModel):
    book_title: str = Field(..., title="book_title", description="책 제목", example="FastAPI Tutorial")
    publication_year: int = Field(..., title="publication_year", description="출판년도", example=2022, ge=0)
    request_link: str = Field(..., title="request_link", description="요청 링크", example="https://example.com/request")
    reason: str = Field(..., title="reason", description="이유", example="Need for study")
