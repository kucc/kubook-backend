from datetime import date

from pydantic import BaseModel, Field


class RouteReqPostAdmin(BaseModel):
  user_id:int = Field(title="user_id", description="관리자의 회원 ID", gt=0)
  admin_status:bool = Field(title="admin_status", description="관리자 권한 상태", examples=[0, 1])
  expire_date: date = Field(title="expiration_date", description="관리자 권한 만료 기한", examples=["2025-08-12"])

class RouteReqPutAdmin(BaseModel):
  admin_status: bool | None = Field(None, title="admin_status", description="관리자 권한 상태", examples=[0, 1])
  expire_date: date | None = Field(None, title="expiration_date", description="관리자 권한 만료 기한", \
                                   examples=["2025-08-12"])
