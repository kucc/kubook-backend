from datetime import datetime as _datetime
from pydantic import Field
from src.core.common import CustomBaseModel

# Review CRUD를 위한 schema 필요


class ReviewBase(CustomBaseModel):
    user_id: int = Field(..., title="user_id", description="유저 id", examples=1, ge=1)
    book_info_id: int = Field(..., title="book_info_id", description="책과 연결된 정보 id", examples=1, ge=1)
    review_content: str = Field(..., title="review_content", description="리뷰 사항", examples="")


class Review(ReviewBase):
    id: int = Field(..., title="review_id", description="책 리뷰 id", example=1, ge=1)
    created_at: _datetime = Field(..., title="create_at", description="생성일시", example=_datetime.now())
    updated_at: _datetime = Field(..., title="update_at", description="수정일시", example=_datetime.now())
    is_valid: bool = Field(..., title="is_valid", description="유효 여부", example=True)
