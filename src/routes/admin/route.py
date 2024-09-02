from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

import domain.schemas.admin_schemas as s
from dependencies import get_current_admin, get_db
from utils.admin_service import *
from repositories.admin_repository import Admin

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_current_admin)]
)

# =================== 관리자 =========================


@router.get(
    "/info",
    summary="관리자 정보 목록 조회",
    response_model=List[s.AdminRes],
    status_code=status.HTTP_200_OK
)
async def get_list_admin(db: Session = Depends(get_db)):
    return get_list(Admin, db)


@router.get(
    "/info/{admin_id}",
    summary="관리자 정보 조회",
    response_model=s.Admin,
    status_code=status.HTTP_200_OK
)
async def get_admin(admin_id: int, db: Session = Depends(get_db)):
    return get_item(Admin, admin_id, db)


@router.post(
    "/info",
    summary="관리자 정보 등록",
    response_model=s.Admin,
    status_code=status.HTTP_201_CREATED
)
async def create_admin(admin_data: s.AdminCreate, db: Session = Depends(get_db)):
    return create_item(Admin, admin_data, db)


@router.patch(
    "/info/{admin_id}",
    summary="관리자 정보 수정",
    response_model=s.Admin,
    status_code=status.HTTP_200_OK
)
async def update_admin(admin_id: int, admin_data: s.AdminUpdate, db: Session = Depends(get_db)):
    return update_item(Admin, admin_id, admin_data, db)


@router.delete(
    "/info/{admin_id}",
    summary="관리자 정보 삭제",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_admin(admin_id: int, db: Session = Depends(get_db)):
    return delete_item(Admin, admin_id, db)
