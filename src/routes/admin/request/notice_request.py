from pydantic import BaseModel, Field


class RouteReqAdminPostNotice(BaseModel):
    title: str = Field(title="title", description="공지사항 제목", examples=["공지사항 제목1"])
    notice_content: str = Field(title="notice content", description="공지사항 내용", examples=["공지사항 내용1"])

class RouteReqAdminPutNotice(BaseModel):
    title: str = Field(title="title", description="공지사항 제목", examples=["공지사항 제목1"])
    notice_content: str = Field(title="notice content", description="공지사항 내용", examples=["공지사항 내용1"])
