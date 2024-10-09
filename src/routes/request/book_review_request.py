from pydantic import BaseModel, Field


class RouteReqPutReview(BaseModel):
    review_content: str = Field(title="review_content", description="리뷰 내용")
#BookReviewUpdateRouteRequest

class RouteReqPostReview(BaseModel):
    book_info_id: int = Field(title="book_info_id", description="리뷰한 책 정보 ID", example=1, gt=0)
    review_content: str = Field(title="review_content", description="리뷰 내용")
