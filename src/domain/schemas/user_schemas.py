from datetime import date

from pydantic import BaseModel, Field


class DomainResGetUser(BaseModel):
    user_id: int = Field(title="user_id", description="유저 고유 ID", example=1111, gt=0)
    auth_id: str = Field(title="auth_id", description="로그인 ID", example="gildong1")
    email: str = Field(title="email", description="이메일 주소", example="KUCC@korea.ac.kr")
    user_name: str = Field(title="user_name", description="사용자 이름", example="홍길동")
    is_active: bool = Field(title="is_active", description="활동 상태", example=1)
    github: str | None = Field(None, title="github", description="깃허브 주소", example="https://github.com/kucc")
    instagram: str | None = Field(None, title="instagram", description="인스타그램 주소", example="https://www.instagram.com/")

class DomainReqPutUser(BaseModel):
    user_id: int = Field(title="user_id", description="유저 고유 ID", example=1111, gt=0)
    user_name: str = Field(title="user_name", description="사용자 이름", example="홍길동")
    github: str | None = Field(None, title="github", description="깃허브 주소", example="https://github.com/kucc")
    instagram: str | None = Field(None, title="instagram", description="인스타그램 주소", example="https://www.instagram.com/")

class DomainResPutUser(BaseModel):
    user_id: int = Field(title="user_id", description="유저 고유 ID", example=1111, gt=0)
    auth_id: str = Field(title="auth_id", description="로그인 ID", example="gildong1")
    email: str = Field(title="email", description="이메일 주소", example="KUCC@korea.ac.kr")
    user_name: str = Field(title="user_name", description="사용자 이름", example="홍길동")
    is_active: bool = Field(title="is_active", description="활동 상태", example=1)
    github: str | None = Field(None, title="github", description="깃허브 주소", example="https://github.com/kucc")
    instagram: str | None = Field(None, title="instagram", description="인스타그램 주소", example="https://www.instagram.com/")

class DomainReqAdminPutUser(BaseModel):
    user_id: int = Field(title="user_id", description="관리자의 회원 ID", gt=0)
    user_status: bool | None = Field(None, title="is_active", description="회원 상태(대출 가능 여부)", examples=[True])
    admin_status: bool | None = Field(None, title="admin_status", description="관리자 권한 상태")
    expiration_date : date | None = Field(None, title="expiration_date", description="관리자 권한 만료일, \
                                          기본적으로 권한 부여일로부터 1년", examples=["2025-07-02"])
class DomainResAdminPutUser(BaseModel):
    user_id: int = Field(title="user_id", description="유저 고유 ID", example=1111, gt=0)
    auth_id: str = Field(title="auth_id", description="로그인 ID", example="gildong1")
    email: str = Field(title="email", description="이메일 주소", example="KUCC@korea.ac.kr")
    user_name: str = Field(title="user_name", description="사용자 이름", example="홍길동")
    is_active: bool = Field(title="is_active", description="활동 상태", examples=[True])
    is_admin: bool = Field(title="is_admin", description="관리자 권환", examples=[False])
    expiration_date : date | None  = Field(title="expiration_date", description="관리자 권한 만료일, \
                                          기본적으로 권한 부여일로부터 1년", examples=["2025-07-02"])
