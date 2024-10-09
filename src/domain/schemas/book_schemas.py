from datetime import datetime as _datetime

from pydantic import BaseModel, Field


class Book(BaseModel):
    id: int = Field(title="book_id", description="도서 id", example=1, gt=0)
    book_info_id: int = Field(title="book_info_id", description="도서 정보 id", example=1, gt=0)
    book_status: bool = Field(title="book_stauts", description="도서 대출 상태", example=True)
    note: str = Field(title="note", description="메모", example="kucc")
    donor_name: str = Field(title="donor_name", description="도서 기증자 성함", example="kucc 부원")
    created_at: _datetime = Field(title="create_at", description="생성일시", example=_datetime.now())
    updated_at: _datetime = Field(title="update_at", description="수정일시", example=_datetime.now())


class DomainResGetBookItem(BaseModel):
    book_id: int = Field(title="book_id", description="도서 id", example=1, gt=0)
    book_info_id: int = Field(title="book_info_id", description="도서 정보 id", example=1, gt=0)
    book_title: str = Field(title="book_title", description="책 제목", example="FastAPI Tutorial")
    category_name: str = Field(title="category_name", description="카테고리 이름", example="웹")
    image_url: str | None = Field(title="image_url", description="도서 표지 이미지")
    book_status: bool = Field(title="book_stauts", description="도서 대출 상태", example=True)
    created_at: _datetime = Field(title="create_at", description="생성일시", example=_datetime.now())
    updated_at: _datetime = Field(title="update_at", description="수정일시", example=_datetime.now())
