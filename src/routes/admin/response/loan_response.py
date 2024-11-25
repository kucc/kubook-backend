from pydantic import BaseModel

from domain.schemas.admin.loan_schema import DomainAdminGetLoanItem


class RouteResAdminGetLoanList(BaseModel):
    data: list[DomainAdminGetLoanItem]
    count: int

