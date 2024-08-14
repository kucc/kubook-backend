from typing import List

import admin.schemas as s
import models as m
from admin.service import *
from dependencies import get_current_admin, get_db
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/admin/notices",
    tags=["admin/notices"],
    dependencies=[Depends(get_current_admin)]
)

@router.get(
    "/",
    summary="전체 공지사항 목록 조회",
    response_model=List[s.NoticeRes],
    status_code=status.HTTP_200_OK
)
async def get_list_notices(db: Session = Depends(get_db)):
    return get_list(m.Notice, db)

@router.get(
    "/{notice_id}",
    summary="공지사항 조회",
    response_model=s.Notice,
    status_code=status.HTTP_200_OK
)
async def get_notice(notice_id: int, db: Session = Depends(get_db)):
    return get_item(m.Notice, notice_id, db)

@router.post(
    "/",
    summary="공지사항 등록",
    response_model=s.Notice,
    status_code=status.HTTP_201_CREATED
)
async def create_notice(notice_data: NoticeCreate, current_user: m.User = Depends(get_current_admin), db: Session = Depends(get_db)):
    notice_data.admin_id = current_user.admin.id
    return create_item(m.Notice, notice_data, db)

@router.patch(
    "/{notice_id}",
    summary="공지사항 수정",
    response_model=s.Notice,
    status_code=status.HTTP_200_OK
)
async def update_notice(notice_id: int, notice_data: NoticeUpdate, current_user: m.User = Depends(get_current_admin), db: Session = Depends(get_db)):
    notice_data.admin_id = current_user.admin.id
    return update_item(m.Notice, notice_id, notice_data, db)

@router.delete(
    "/{notice_id}",
    summary="공지사항 삭제",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_notice(notice_id: int, db: Session = Depends(get_db)):
    return delete_item(m.Notice, notice_id, db)