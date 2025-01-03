from pydantic import BaseModel

from domain.schemas.loan_schemas import DomainResAdminGetLoan


class RouteResAdminGetLoanList(BaseModel):
    data: list[DomainResAdminGetLoan]
    count: int
    total: int

