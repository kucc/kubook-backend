from datetime import datetime as _datetime

from pydantic import BaseModel, Field


class DomainResGetReviewByInfoId(BaseModel):
    review_id: int = Field(title="book_review_id", description="리뷰 id", example=1, gt=0)
    user_id: int = Field(title="user_id", description="리뷰한 사용자 ID", example=1, gt=0)
    user_name: str = Field(title="user_name", description="리뷰한 사용자 이름", example="test")
    review_content: str = Field(title="review_content", description="리뷰 내용")
    created_at: _datetime = Field(title="create_at", description="생성일시", example=_datetime.now())
    updated_at: _datetime = Field(title="update_at", description="수정일시", example=_datetime.now())


class Review(BaseModel):
    id: int = Field(title="book_review_id", description="리뷰 정보 id", example=1, gt=0)
    user_id: int = Field(title="user_id", description="리뷰한 사용자 ID", example=1, gt=0)
    book_info_id: int = Field(title="book_info_id", description="리뷰한 책 정보 ID", example=1, gt=0)
    review_content: str = Field(title="review_content", description="리뷰 내용")
    created_at: _datetime = Field(title="create_at", description="생성일시", example=_datetime.now())
    updated_at: _datetime = Field(title="update_at", description="수정일시", example=_datetime.now())


class DomainResGetReviewItem(BaseModel):
    review_id: int = Field(title="book_review_id", description="리뷰 id", example=1, gt=0)
    user_id: int = Field(title="user_id", description="리뷰한 사용자 ID", example=1, gt=0)
    book_info_id: int = Field(title="book_info_id", description="리뷰한 책 정보 ID", example=1, gt=0)
    review_content: str = Field(title="review_content", description="리뷰 내용")
    created_at: _datetime = Field(title="create_at", description="생성일시", example=_datetime.now())
    updated_at: _datetime = Field(title="update_at", description="수정일시", example=_datetime.now())


class DomainReqPostReview(BaseModel):
    user_id: int = Field(title="user_id", description="리뷰한 사용자 ID", example=1, gt=0)
    book_info_id: int = Field(title="book_info_id", description="리뷰한 책 정보 ID", example=1, gt=0)
    review_content: str = Field(title="review_content", description="리뷰 내용")


class DomainResPostReview(BaseModel):
    review_id: int = Field(title="book_review_id", description="리뷰 id", example=1, gt=0)
    user_id: int = Field(title="user_id", description="리뷰한 사용자 ID", example=1, gt=0)
    user_name: str = Field(title="user_name", description="리뷰한 사용자 이름")
    book_info_id: int = Field(title="book_info_id", description="리뷰한 책 정보 ID", example=1, gt=0)
    review_content: str = Field(title="review_content", description="리뷰 내용")
    created_at: _datetime = Field(title="create_at", description="생성일시", example=_datetime.now())

class DomainReqPutReview(BaseModel):
    review_id: int = Field(title="book_review_id", description="리뷰 id", example=1, gt=0)
    user_id: int = Field(title="user_id", description="리뷰한 사용자 ID", example=1, gt=0)
    review_content: str = Field(title="review_content", description="리뷰 내용")
