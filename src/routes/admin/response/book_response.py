from pydantic import BaseModel

from domain.schemas.admin.book_schema import DomainAdminGetBookItem


class RouteResAdminGetBookList(BaseModel):
    data: list[DomainAdminGetBookItem]
    count: int

