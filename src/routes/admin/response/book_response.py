from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class RouteResAdminPostBook(BaseModel):
  book_id: int = Field(title="book_id", description="책 ID", gt=0)
  book_title: str = Field(title="book_title", description="책 제목", example="FastAPI Tutorial")
  code: str = Field(title="code", description="책 코드", examples="A3")
  category_name: str = Field(title="category_name", description="카테고리명", examples="웹")
  subtitle: Optional[str] = Field(title="subtitle", description="책 부제", default=None)
  author : str = Field(title="author", description="저자")
  publisher: str = Field(title="publisher", description="출판사")
  publication_year: int = Field(title="publication_year", description="출판연도", gt=0)
  image_url: Optional[str] = Field(title="image_url", description="책 표지", default=None)
  version: Optional[str] = Field(title="version", description="판본", default=None)
  major: bool = Field(title="major", description="전공 책 여부", default=False)
  language: str = Field(title="language", description="언어", default="KOREAN")
  book_status : bool = Field(title="book_status", description="도서 상태", default=True)
  donor_name: Optional[str] = Field(title="donor_name", description="기부자명", default=None)
  created_at: datetime = Field(title="create_at", description="생성일시", example=datetime.now())
  updated_at: datetime = Field(title="update_at", description="수정일시", example=datetime.now())
