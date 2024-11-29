
from typing import Self

from fastapi import HTTPException, status
from pydantic import BaseModel, Field, model_validator


class RouteReqAdminPutBookRequest(BaseModel):
    processing_status: int = Field(0, title="processing_status", description="처리 상태", example=0)
    reject_reason: str | None = Field(None, title="reject_reason", description="거절 사유", example="Not available")

    @model_validator(mode='after')
    def check_reject_reason(self) -> Self:
        if self.processing_status == 3 and not self.reject_reason:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Reject reason is missed"
            )
        return self
