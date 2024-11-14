from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from dependencies import get_current_admin, get_db
from domain.services.admin.user_service import service_admin_read_users
from routes.admin.response.user_response import RouteResAdminGetUserList

router = APIRouter(
    prefix="/admin/users",
    tags=["admin"],
    dependencies=[Depends(get_current_admin)]
)


@router.get(
    "/search",
    response_model=RouteResAdminGetUserList,
    status_code=status.HTTP_200_OK,
    summary="전체 사용자 목록 조회",
)
async def get_all_users(
    db: Session = Depends(get_db),
    user_name: str = Query(description="사용자 이름", example="test"),
    authority: bool = Query(description="권한 여부", example=False, default=False),
    active: bool = Query(description="관리자 활성 여부", example=False, default=False),
    current_user=Depends(get_current_admin)
):
    response = await service_admin_read_users(user_name, authority, active, db)

    return response
