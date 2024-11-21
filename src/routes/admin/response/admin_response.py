from datetime import date, datetime

from pydantic import BaseModel, Field


class RouteResAdmin(BaseModel):
  admin_id: int = Field(title="admin_id", description="관리자 ID", gt=0)
  user_id:int = Field(title="user_id", description="관리자의 회원 ID",  gt=0)
  admin_status:bool = Field(title="admin_status", description="관리자 권한 상태", examples=[0, 1])
  expire_date: date = Field(title="expiration_date", description="관리자 권한 만료 기한", examples=["2025-08-12"])
  created_at: datetime = Field(title="created_at", description="생성일시", example=datetime.now())
  updated_at: datetime = Field(title="updated_at", description="수정일시", example=datetime.now())

class RouteResGetAdminList(BaseModel):
  data : list[RouteResAdmin]
  count : int
