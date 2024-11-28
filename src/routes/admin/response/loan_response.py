from pydantic import BaseModel

from domain.schemas.loan_schemas import DomainAdminGetLoanItem


class RouteResAdminGetLoanList(BaseModel):
    data: list[DomainAdminGetLoanItem]
    count: int

