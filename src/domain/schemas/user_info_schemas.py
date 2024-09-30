from pydantic import BaseModel, Field
from typing import Optional

class DomainReqGetUser_Info(BaseModel):
    user_id: int = Field(..., title="user_id", description="유저 고유 ID", example=1111, gt=0)

class DomainResGetUser_Info(BaseModel):
    user_id: int = Field(..., title="user_id", description="유저 고유 ID", example=1111, gt=0)
    auth_id: str = Field(..., title="auth_id", description="로그인 ID", example="gildong1")
    email: str = Field(..., title="email", description="이메일 주소", example="KUCC@korea.ac.kr")
    user_name: str = Field(..., title="user_name", description="사용자 이름", example="홍길동")
    is_active: bool = Field(..., title="is_active", description="활동 상태", example=1)
    github: Optional[str] = Field(None, title="github", description="깃허브 주소", example="https://github.com/kucc")
    instagram: Optional[str] = Field(None, title="instagram", description="인스타그램 주소", example="https://www.instagram.com/")

class DomainReqPutUser_Info(BaseModel):
    user_id: int = Field(..., title="user_id", description="유저 고유 ID", example=1111, gt=0)
    user_name: str = Field(..., title="user_name", description="사용자 이름", example="홍길동", gt = 0)
    github: Optional[str] = Field(None, title="github", description="깃허브 주소", example="https://github.com/kucc")
    instagram: Optional[str] = Field(None, title="instagram", description="인스타그램 주소", example="https://www.instagram.com/")
    
class DomainReqPutUser_Info(BaseModel):
    user_id: int = Field(..., title="user_id", description="유저 고유 ID", example=1111, gt=0)
    auth_id: str = Field(..., title="auth_id", description="로그인 ID", example="gildong1", gt = 0)
    email: str = Field(..., title="email", description="이메일 주소", example="KUCC@korea.ac.kr", gt = 0)
    user_name: str = Field(..., title="user_name", description="사용자 이름", example="홍길동", gt = 0)
    is_active: bool = Field(..., title="is_active", description="활동 상태", example=1)
    github: Optional[str] = Field(None, title="github", description="깃허브 주소", example="https://github.com/kucc")
    instagram: Optional[str] = Field(None, title="instagram", description="인스타그램 주소", example="https://www.instagram.com/")