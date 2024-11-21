from datetime import date

from pydantic import BaseModel, Field

from domain.schemas.notice_schemas import DomainResGetNotice


class RouteResGetNotice(BaseModel):
    notice_id: int = Field(title="notice_id", description="공지사항 ID", example=1, gt=0)
    admin_id: int = Field(title="admin_id", description="관리자 ID", example=1, gt=0)
    admin_name: str = Field(title="admin_id", description="관리자 성명", example="관리자 성명")
    title: str = Field(title="title", description="공지사항 제목", example="공지사항 제목")
    notice_content: str = Field(title="notice content", description="공지사항 내용", example="공지사항 내용")
    created_at: date = Field(title="created_at", description="공지사항 생성일", example=date.today())

class RouteResGetNoticeList(BaseModel):
    data: list[DomainResGetNotice]
    total: int

