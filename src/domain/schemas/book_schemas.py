from datetime import datetime as _datetime
from typing import Optional

from pydantic import BaseModel, Field

# TODO : GET REQUEST에 대한 RESPONSE SCHEMA 구현
# - BookInfo, Book, Category, Review schema를 활용
# - Review schma 구현 필요


class BookInfoBase(BaseModel):
    title: str = Field(..., title="title", description="책 제목", example="FastAPI Tutorial")
    subtitle: Optional[str] = Field(None, title="subtitle", description="책 부제목", example="Build modern web APIs with Python and FastAPI")
    author: str = Field(..., title="author", description="저자", example="John Doe")
    publisher: str = Field(..., title="publisher", description="출판사", example="AA Publisher")
    publication_year: int = Field(..., title="publication_year", description="출판년도", example=_datetime.now().year)
    image_url: Optional[str] = Field(None, title="image_url", description="이미지 URL", example="https://example.com/image.jpg")
    category_id: int = Field(..., title="category_id", description="카테고리 ID", example=1, ge=0)
    version: Optional[str] = Field(None, title="version", description="책 버전", example="1판")
    major: Optional[bool] = Field(False, title="major", description="전공 도서 여부", example=False)
    language: Optional[bool] = Field(True, title="language", description="True: 국문, False: 영문", example=True)


class BookInfo(BookInfoBase):
    id: int = Field(..., title="book_info_id", description="도서 정보 id", example=1, ge=0)
    created_at: _datetime = Field(..., title="create_at", description="생성일시", example=_datetime.now())
    updated_at: _datetime = Field(..., title="create_at", description="수정일시", example=_datetime.now())
    is_valid: bool = Field(..., title="is_valid", description="유효 여부", example=True)


class BookBase(BaseModel):
    book_info_id: int = Field(..., title="book_info_id", description="책과 연결된 도서 정보 id", example=1, ge=0)
    book_status: int = Field(0, title="book_status", description="책 상태", example=1, le=0, ge=3)
    note: Optional[str] = Field(None, title="note", description="노트", example="기부된 책")
    donor_name: Optional[str] = Field(None, title="donor_name", description="기부자 이름", example="김철수")


class Book(BookBase):
    id: int = Field(..., title="book_id", description="책 정보 id", example=1, ge=0)
    created_at: _datetime = Field(..., title="create_at", description="생성일시", example=_datetime.now())
    updated_at: _datetime = Field(..., title="update_at", description="수정일시", example=_datetime.now())


class CategoryBase(BaseModel):
    code: str = Field(..., title="code", description="카테고리 코드", example="A")
    name: str = Field(..., title="name", description="카테고리명", example="인공지능")


class Category(CategoryBase):
    id: int = Field(..., title="category_id", description="카테고리 id", example=1, ge=0)
    created_at: _datetime = Field(..., title="create_at", description="생성일시", example=_datetime.now())
    updated_at: _datetime = Field(..., title="update_at", description="수정일시", example=_datetime.now())
    is_valid: bool = Field(..., title="is_valid", description="유효 여부", example=True)
