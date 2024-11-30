from datetime import date, datetime

from fastapi import HTTPException, status
from pydantic import BaseModel, Field, model_validator


class RouteReqAdminPutUser(BaseModel):
    user_status: bool | None = Field(None, title="is_active", description="회원 상태(대출 가능 여부)", examples=[True])
    admin_status: bool | None = Field(None, title="admin_status", description="관리자 권한 상태", examples=[True])
    expiration_date: date | None = Field(None, title="expiration_date", description="관리자 권한 만료일", \
                                         examples=[datetime(2025, 7, 2).date()])
    @model_validator(mode="after")
    def check_at_least_one_field(cls, values):
        # If all three fields are None, raise an error
        if all(values is None for values in RouteReqAdminPutUser.model_fields):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="At least one field must be provided."
            )
        return values
