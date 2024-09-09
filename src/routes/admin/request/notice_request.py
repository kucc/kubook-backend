from pydantic import Field, BaseModel


class NoticeRequest(BaseModel):
    title: str = Field(title="title", description="공지 제목", examples=["점검 기간 안내"])
    content: str = Field(title="content", description="공지 내용", examples=["점검 기간 서비스 운영이 일시 중지됩니다"])
