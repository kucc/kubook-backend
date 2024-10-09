from pydantic import BaseModel, Field


class RouteReqPostLoan(BaseModel):
    book_id: int = Field(title="book_id", description="대출한 책 ID", example=1, gt=0)
