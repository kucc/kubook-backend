from datetime import datetime as _datetime

from pydantic import BaseModel, Field


class UserBase(BaseModel):
    user_name: str = Field(..., title="user_name", description="사용자 이름", example="JohnDoe")
    is_active: bool = Field(True, title="is_active", description="활성 상태", example=True)
    email: str = Field(..., title="email", description="이메일", example="john.doe@example.com")


class User(UserBase):
    id: int = Field(..., title="user_id", description="사용자 ID", example=1, ge=0)
    created_at: _datetime = Field(..., title="create_at", description="생성일시", example=_datetime.now())
    updated_at: _datetime = Field(..., title="update_at", description="수정일시", example=_datetime.now())
