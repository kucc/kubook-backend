from fastapi import HTTPException, status
from pydantic import BaseModel, Field, field_validator, model_validator
from typing_extensions import Self

from domain.enums.status import BookRequestStatus


class RouteReqAdminPutBookRequest(BaseModel):
    processing_status: int = Field(0, title="processing_status", description="처리 상태", example=0)
    reject_reason: str | None = Field(None, title="reject_reason", description="거절 사유", example="Not available")

    @field_validator("processing_status")
    @classmethod
    def valid_status(cls, processing_status):
        if not BookRequestStatus.is_valid_enum_value(processing_status):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid processing status"
            )
        return processing_status

    @model_validator(mode='after')
    def check_reject_reason(self) -> Self:
        if self.processing_status == BookRequestStatus.REJECTED() and not self.reject_reason:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Reject reason is missed"
            )
        return self
