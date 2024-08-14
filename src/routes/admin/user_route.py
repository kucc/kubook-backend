from typing import List

import admin.schemas as s
import models as m
from admin.service import *
from dependencies import get_current_admin, get_db
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/admin/users",
    tags=["admin/users"],
    dependencies=[Depends(get_current_admin),]
)

@router.get(
    "/",
    summary="전체 사용자 목록 조회",
    response_model=List[s.UserRes],
    status_code=status.HTTP_200_OK
)
async def get_list_user( db: Session = Depends(get_db)):
    return get_list(m.User, db)

@router.get(
    "/{user_id}",
    summary="사용자 정보 조회",
    response_model=s.UserRes,
    status_code=status.HTTP_200_OK
)
async def get_user(user_id: int,  db: Session = Depends(get_db)):
    return get_item(m.User, user_id, db)

@router.patch(
    "/{user_id}",
    summary="사용자 정보 수정",
    description = "이름, 활동상태, 이메일 정보 수정 시 사용",
    response_model=s.UserRes,
    status_code=status.HTTP_200_OK
)
async def update_user(user_id: int, user: s.UserUpdate,  db: Session = Depends(get_db)):
    return update_item(m.User, user_id, user, db)

@router.delete(
    "/{user_id}",
    summary="사용자 정보 삭제",
    description="사용자 탈퇴 시 사용",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_user(user_id: int,  db: Session = Depends(get_db)):

    user_admin = get_item_by_column(model=m.Admin, columns={"user_id": user_id}, db=db)

    if(user_admin[0] != None) : 
        user_admin_id:int = user_admin[0].id
        admin:AdminUpdate = {"admin_status" : False}
        update_item(m.Admin, user_admin_id, admin, db)
        delete_item(m.Admin, user_admin_id, db)
    
    user:UserUpdate = {"is_active" : False}
    update_item(m.User, user_id, user, db)
    return delete_item(m.User, user_id, db)
