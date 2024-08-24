from datetime import date
from datetime import datetime as _datetime

from pydantic import BaseModel, Field


class ReservationBase(BaseModel):
    book_id: int = Field(..., title="book_id", description="예약한 책 ID", example=1, ge=0)
    user_id: int = Field(..., title="user_id", description="예약한 사용자 ID", example=1, ge=0)
    reservation_date: date = Field(..., title="reservation_date", description="예약 날짜", example=_datetime.now().date())
    reservation_status: int = Field(0, title="reservation_status", description="예약 상태", example=0, ge=0, le=3)


class Reservation(ReservationBase):
    id: int = Field(..., title="reservation_id", description="예약 정보 ID", example=1, ge=0)
    created_at: _datetime = Field(..., title="create_at", description="생성일시", example=_datetime.now())
    updated_at: _datetime = Field(..., title="update_at", description="수정일시", example=_datetime.now())


class ReservationCreate(ReservationBase.omit_fields("ReservationCreate", ["reservation_date", "reservation_status"])):
    pass


class ReservationUpdate(ReservationBase.all_optional("ReservationUpdate")):
    pass
