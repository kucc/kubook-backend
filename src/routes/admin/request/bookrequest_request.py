
from pydantic import BaseModel, Field


class RouteReqAdminPutBookRequest(BaseModel):
    processing_status: int = Field(0, title="processing_status", description="처리 상태", example=0, ge=0, le=3)
    reject_reason: str | None = Field(None, title="reject_reason", description="거절 사유", example="Not available")
