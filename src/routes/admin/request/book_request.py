from pydantic import BaseModel, Field


class RouteReqAdminPostBook(BaseModel):
    book_title: str = Field(title="book_title", description="책 제목", example="FastAPI Tutorial")
    code: str = Field(title="code", description="책 코드", examples="A3")
    category_name: str = Field(title="category_name", description="카테고리명", examples="웹")
    subtitle: str | None = Field(title="subtitle", description="책 부제")
    autor : str = Field(title="author", description="저자")
    publisher: str = Field(title="publisher", description="출판사")
    publication_year: int = Field(title="publication_year", description="출판연도", gt=0)
    image_url: str | None = Field(title="image_url", description="책 표지")
    version: str | None = Field(title="version", description="판본")
    major: bool = Field(title="major", description="전공 책 여부")
    language: str = Field(title="language", description="언어")
    donor_name: str | None = Field(title="donor_name", description="기부자명")
