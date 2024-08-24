from fastapi import APIRouter, Depends

from dependencies import get_current_admin
from domain.services.admin_service import *

router = APIRouter(
    prefix="/admin/settings",
    tags=["admin/settings"],
    dependencies=[Depends(get_current_admin)]
)

# @router.get(
#     "/",
#     summary="전체 시스템 설정 목록 조회",
#     response_model=List[s.ServiceSetting],
#     status_code=status.HTTP_200_OK
# )
# async def list_get_settings(db: Session = Depends(get_db)):
#     return get_list(m.LibrarySetting, db)


# @router.get(
#     "/{setting_id}",
#     summary="시스템 설정 조회",
#     response_model=s.ServiceSetting,
#     status_code=status.HTTP_200_OK
# )
# async def get_settings(setting_id: int, db: Session = Depends(get_db)):
#     return get_item(m.LibrarySetting, setting_id, db)

# @router.post(
#     "/",
#     summary="시스템 설정 등록",
#     response_model=s.ServiceSetting,
#     status_code=status.HTTP_201_CREATED
# )
# async def create_settings(settings: ServiceSettingCreate, db: Session = Depends(get_db)):
#     return create_item(m.LibrarySetting, settings, db)


# @router.patch(
#     "/{setting_id}",
#     summary="시스템 설정 수정",
#     response_model=s.ServiceSetting,
#     status_code=status.HTTP_200_OK
# )
# async def update_settings(setting_id: int, setting: ServiceSettingUpdate, db: Session = Depends(get_db)):
#     return update_item(m.LibrarySetting, setting_id, setting, db)

# @router.delete(
#     "/{setting_id}",
#     summary="시스템 설정 삭제",
#     status_code=status.HTTP_204_NO_CONTENT
# )
# async def delete_settings(setting_id: int, db: Session = Depends(get_db)):
#     return delete_item(m.LibrarySetting, setting_id, db)
