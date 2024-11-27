from pydantic import BaseModel

from domain.schemas.user_schemas import DomainAdminGetUserItem


class RouteResAdminGetUserList(BaseModel):
    data: list[DomainAdminGetUserItem]
    count: int
