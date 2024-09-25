from pydantic import BaseModel, Field


class BookReviewUpdateRouteRequest(BaseModel):
    review_content: str = Field(title="review_content", description="리뷰 내용")
