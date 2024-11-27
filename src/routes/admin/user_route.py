from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query, status
from sqlalchemy.orm import Session

from dependencies import get_current_admin, get_db
from domain.schemas.user_schemas import DomainReqAdminDelUser
from domain.services.admin.user_service import (
    service_admin_delete_user,
    service_admin_read_users,
    service_admin_search_users,
)
from routes.admin.response.user_response import RouteResAdminGetUserList

router = APIRouter(
    prefix="/admin/users",
    tags=["admin/users"],
    dependencies=[Depends(get_current_admin)]
)

@router.get(
    "/search",
    response_model=RouteResAdminGetUserList,
    status_code=status.HTTP_200_OK,
    summary="전체 사용자 목록 검색",
)
async def search_users(
    db: Session = Depends(get_db),
    user_name: Annotated[
        str, Query(description="사용자 이름", example="test")
    ] = None,
    authority: Annotated[
        bool, Query(description="권한 여부", example=False)
    ] = None,
    active: Annotated[
        bool, Query(description="관리자 활성 여부", example=False)
    ] = None,
    current_user: Annotated = Depends(get_current_admin)
):
    response = await service_admin_search_users(
        user_name=user_name,
        authority=authority,
        active=active,
        db=db
    )

    result = RouteResAdminGetUserList(
        data=response,
        count=len(response)
    )

    return result


@router.get(
    "/",
    response_model=RouteResAdminGetUserList,
    status_code=status.HTTP_200_OK,
    summary="전체 사용자 목록 조회",
)
async def get_all_users(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_admin)
):
    response = await service_admin_read_users(
        db=db
    )

    result = RouteResAdminGetUserList(
        data=response,
        count=len(response)
    )

    return result


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="회원 탈퇴",
)
async def delete_user(
    user_id: Annotated[int, Path(description="삭제할 사용자 ID")],
    db: Session = Depends(get_db),
    current_user=Depends(get_current_admin)
):
    domain_req = DomainReqAdminDelUser(
        user_id=user_id
    )
    await service_admin_delete_user(domain_req, db)
    return
