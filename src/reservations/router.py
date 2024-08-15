from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from dependencies import get_db, get_current_active_user

router = APIRouter(
    prefix="/reservations",
    tags=["reservations"]
)


@router.post(
    "/",
    summary="도서 예약 신청 새로 추가한 부분 ㅇㅅㅇ",
)
async def create_reservation(db: Session = Depends(get_db), current_user=Depends(get_current_active_user)):
    pass

print("예약 신청 부분 추가")


@router.get(
    "/",
    summary="예약 목록 조회",
)
async def list_reservations(db: Session = Depends(get_db), current_user=Depends(get_current_active_user)):
    pass


@router.get(
    "/{reservation_id}",
    summary="예약 상세 정보 조회",
)
async def get_reservation(db: Session = Depends(get_db), current_user=Depends(get_current_active_user)):
    pass


@router.delete(
    "/{reservation_id}",
    summary="예약 취소",
)
async def delete_reservation(db: Session = Depends(get_db), current_user=Depends(get_current_active_user)):
    pass
