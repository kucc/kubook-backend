from pydantic import BaseModel, Field

from domain.schemas.book_schemas import DomainResGetBookItem


class RouteResGetBookList(BaseModel):
    data: list[DomainResGetBookItem]
    count: int = Field(description="data 배열의 요소 개수")

