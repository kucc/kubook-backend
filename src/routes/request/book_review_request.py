from pydantic import BaseModel, Field


class RouteReqPutReview(BaseModel):
    review_content: str = Field(title="review_content", description="리뷰 내용")


# BookReviewUpdateRouteRequest


class RouteReqPostReview(BaseModel):
    book_id: int = Field(title="book_id", description="리뷰한 책 ID", example=1, gt=0)
    review_content: str = Field(title="review_content", description="리뷰 내용")
