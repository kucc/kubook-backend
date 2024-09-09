from typing import List
from pydantic import Field, BaseModel
from domain.schemas.notice_schemas import NoticeResponse


# class NoticeResponse(BaseModel):
#     notice_id: int = Field(title="notice ID", description="공지사항 ID", examples=[1], ge=1)
#     title: str = Field(title="title", description="공지 제목", examples=["점검 기간 안내"])
#     content: str = Field(title="content", description="공지 내용", examples=["점검 기간 서비스 운영이 일시 중지됩니다"])
#     admin_id: int = Field(title="admin ID", description="관리자(작성자) ID", examples=[1], ge=1)
#     author_name: str = Field(title="admin name", description="관리자(작성자) 이름", examples=["김철수"])


class NoticeListResponse(BaseModel):
    data: List[NoticeResponse]
    count: int = Field(title="lenth of data", description="data 배열의 길이", examples=[2], gt=0)
