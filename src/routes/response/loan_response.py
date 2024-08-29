from typing import List
from pydantic import BaseModel, Field

from domain.schemas.loan_schemas import LoanItem


class LoanListResponse(BaseModel):
    data: List[LoanItem]
    count: int = Field(description="data 배열의 요소 개수")
