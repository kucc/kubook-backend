from pydantic import BaseModel

from domain.schemas.admin.user_schema import DomainAdminGetUserItem


class RouteResAdminGetUserList(BaseModel):
    data: list[DomainAdminGetUserItem]
    count: int
