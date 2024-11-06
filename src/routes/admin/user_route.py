from fastapi import APIRouter, Depends, Path, status
from sqlalchemy.orm import Session

from dependencies import get_current_active_user, get_db
from domain.services.admin.user_service import service_admin_read_users
from routes.admin.response.user_response import RouteResAdminGetUserList

router = APIRouter(
    prefix="/admin/users",
    tags=["admin"],
    dependencies=[Depends(get_current_active_user)]
)
"""
    get_current_admin이 미완성이라 get_current_active_user에 의존성 주입함.
"""

@router.get(
    "/{user_name}",
    response_model=RouteResAdminGetUserList,
    status_code=status.HTTP_200_OK,
    summary="전체 사용자 목록 조회",
)
async def get_all_loans(
    db: Session = Depends(get_db),
    user_name: str = Path(description="사용자 이름", example="test"),
    current_user=Depends(get_current_active_user)
):
    response = await service_admin_read_users(user_name, db)

    return response
