from datetime import datetime

from pydantic import BaseModel, Field


class RouteAdminsGetUserItem(BaseModel):
    user_id: int = Field(title="user_id", description="대출한 사용자 ID", example=1, gt=0)
    auth_id: str = Field(title="auth_id", description="인증 ID", max_length=255)
    auth_type: str = Field(default="FIREBASE", description="인증 타입", max_length=20)
    email: str = Field(title="email", description="이메일", max_length=100)
    user_name: str = Field(title="user_name", description="사용자 이름", max_length=45)
    github_id: str | None = Field(default=None, title="github_id", description="깃허브 ID", max_length=100)
    instagram_id: str | None = Field(default=None, title="instagram_id", description="인스타그램 ID", max_length=100)
    is_active: bool = Field(title="is_active", description="활동 상태")
    created_at: datetime = Field(title="create_at", description="생성일시")
    updated_at: datetime = Field(title="update_at", description="수정일시")


class RouteResAdminGetUserList(BaseModel):
    data: list[RouteAdminsGetUserItem]
    count: int
