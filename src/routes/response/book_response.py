from pydantic import BaseModel, Field

from domain.schemas.book_schemas import DomainResGetBookItem


class RouteResGetBookList(BaseModel):
    data: list[DomainResGetBookItem]
    count: int = Field(description="data 배열의 요소 개수")
    total: int = Field(description="객체의 총 요소 개수")


class RouteResGetBook(BaseModel):
    book_id: int = Field(title="book_id", description="책 ID", example=1, gt=0)
    book_title: str = Field(title="book_title", description="책 제목", example="FastAPI Tutorial")
    loanable: bool = Field(title="loanable", description="대출 가능 여부", default=True)
    code: str = Field(title="code", description="책 코드", example="A3")
    category_name: str = Field(title="category_name", description="카테고리 이름", example="웹")
    subtitle: str | None = Field(title="subtitle", description="부제목", example="for beginner")
    author: str = Field(title="author", description="저자", example="minjae")
    publisher: str = Field(title="publisher", description="출판사", example="KUCC")
    publication_year: int = Field(title="publication_year", description="출판년도", example=2022, gt=0)
    image_url: str | None = Field(title="image_url", description="책 이미지 링크", example="https://example.com/img")
    version: str | None = Field(title="version", description="판본", example="10e")
    major: bool | None = Field(title="major", description="전공책 여부", example=True)
    language: str = Field(title="language", description="언어", example="영문")
    donor_name: str | None = Field(title="donor_name", description="책 기증자 성함", example="김철수")
    book_status: bool = Field(title="book_stauts", description="책 상태", example=True)

