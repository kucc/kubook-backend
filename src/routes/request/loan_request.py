from pydantic import BaseModel, Field


class LoanExtendRequest(BaseModel):
    loan_id: int = Field(title="loan_id", description="대출 정보 id", example=1, ge=0)
    user_id: int = Field(title="user_id", description="대출한 사용자 ID", example=1, ge=0)
