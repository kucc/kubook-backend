from datetime import datetime as _datetime

from typing import List
from pydantic import BaseModel, Field

from domain.schemas.book_review_schemas import BookReviewItem


class BookReviewListResponse(BaseModel):
    """
    ReviewListResponse 모델은 리뷰 항목들의 목록과 해당 목록에 포함된 항목 개수를 반환하는 응답 구조입니다.

    Attributes:
        data (List[BookReviewItem]): 리뷰 항목의 목록을 담고 있는 배열입니다.
        count (int): data 배열의 요소 개수를 나타냅니다.
    """
    data: List[BookReviewItem]
    count: int = Field(description="data 배열의 요소 개수")
