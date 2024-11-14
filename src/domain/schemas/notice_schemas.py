from datetime import date

from pydantic import BaseModel, Field


class DomainResAdminGetNotice(BaseModel):
    notice_id: int = Field(title="notice_id", description="공지사항 ID", example=1, gt=0)
    admin_id: int = Field(title="admin_id", description="관리자 ID", example=1, gt=0)
    admin_name: str = Field(title="admin_id", description="관리자 성명", example="관리자 성명")
    title: str = Field(title="title", description="공지사항 제목", example="공지사항 제목")
    notice_content: str = Field(title="notice content", description="공지사항 내용", example="공지사항 내용")
    created_at: date = Field(title="created_at", description="공지사항 생성일", example=date.today())

class DomainResGetNotice(BaseModel):
    notice_id: int = Field(title="notice_id", description="공지사항 ID", example=1, gt=0)
    admin_id: int = Field(title="admin_id", description="관리자 ID", example=1, gt=0)
    admin_name: str = Field(title="admin_id", description="관리자 성명", example="관리자 성명")
    title: str = Field(title="title", description="공지사항 제목", example="공지사항 제목")
    notice_content: str = Field(title="notice content", description="공지사항 내용", example="공지사항 내용")
    created_at: date = Field(title="created_at", description="공지사항 생성일", example=date.today())

class DomainReqAdminPostNotice(BaseModel):
    admin_id: int = Field(title="user_id", description="관리자 ID", example=1, gt=0)
    title: str = Field(title="title", description="공지사항 제목", examples=["공지사항 제목1"])
    notice_content: str = Field(title="notice content", description="공지사항 내용", examples=["공지사항 내용1"])

class DomainResAdminPostNotice(BaseModel):
    notice_id: int = Field(title="notice_id", description="공지사항 ID", examples=[1, 2, 3], gt=0)
    user_name: str = Field(title="user_name", description="사용자 성명", examples=["사용자1", "사용자2"])
    title: str = Field(title="title", description="공지사항 제목", examples=["공지사항 제목1", "공지사항 제목2"])
    notice_content: str = Field(title="notice content", description="공지사항 내용", examples=["공지사항 내용1"])
    created_at: date = Field(title="created_at", description="공지사항 생성일", examples=[date.today()])

class DomainReqAdminPutNotice(BaseModel):
    notice_id: int = Field(title="notice_id", description="공지사항 ID", example=1, gt=0)
    admin_id: int = Field(title="admin_id", description="관리자 ID", example=1, gt=0)
    title: str = Field(title="title", description="공지사항 제목", examples=["공지사항 제목1"])
    notice_content: str = Field(title="notice content", description="공지사항 내용", examples=["공지사항 내용1"])

class DomainResAdminPutNotice(BaseModel):
    notice_id: int = Field(title="notice_id", description="공지사항 ID", examples=[1, 2, 3], gt=0)
    user_name: str = Field(title="user_name", description="사용자 성명", examples=["사용자1", "사용자2"])
    title: str = Field(title="title", description="공지사항 제목", examples=["공지사항 제목1", "공지사항 제목2"])
    notice_content: str = Field(title="notice content", description="공지사항 내용", examples=["공지사항 내용1"])
    created_at: date = Field(title="created_at", description="공지사항 생성일", examples=[date.today()])
