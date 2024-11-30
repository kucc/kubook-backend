from pydantic import BaseModel

from domain.schemas.loan_schemas import DomainAdminGetLoan


class RouteResAdminGetLoanList(BaseModel):
    data: list[DomainAdminGetLoan]
    count: int

