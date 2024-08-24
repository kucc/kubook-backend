from fastapi import APIRouter, Depends

from dependencies import get_current_admin
from domain.services.admin_service import *

router = APIRouter(
    prefix="/admin/reservation",
    tags=["admin/reservation"],
    dependencies=[Depends(get_current_admin)]
)


# @router.get(
#     "/",
#     summary="전체 예약 목록 조회",
#     response_model=List[s.ReservationRes],
#     status_code=status.HTTP_200_OK
# )
# async def get_list_reservations(db: Session = Depends(get_db)):
#     return get_list(m.Reservation, db)


# @router.get(
#     "/{reservation_id}",
#     summary="예약 정보 조회",
#     response_model=s.Reservation,
#     status_code=status.HTTP_200_OK
# )
# async def get_reservation(reservation_id: int,  db: Session = Depends(get_db)):
#     return get_item(m.Reservation, reservation_id, db)


# @router.patch(
#     "/{reservation_id}",
#     summary="예약 정보 수정",
#     response_model=s.Reservation,
#     status_code=status.HTTP_200_OK
# )
# async def update_reservation(reservation_id: int, reservation_data: ReservationUpdate,  db: Session = Depends(get_db)):
#     return update_item(m.Reservation, reservation_id, reservation_data, db)


# @router.delete(
#     "/{reservation_id}",
#     summary="예약 정보 삭제",
#     status_code=status.HTTP_204_NO_CONTENT
# )
# async def delete_reservation(reservation_id: int,  db: Session = Depends(get_db)):
#     return delete_item(m.Reservation, reservation_id, db)
