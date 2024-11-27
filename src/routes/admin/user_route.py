from typing import Annotated

from fastapi import APIRouter, Depends, Path, status
from sqlalchemy.orm import Session

from dependencies import get_current_admin, get_db
from domain.schemas.user_schemas import DomainReqAdminDelUser
from domain.services.admin.user_service import service_admin_delete_user

router = APIRouter(
    prefix="/admin/users",
    tags=["admin/users"],
    dependencies=[Depends(get_current_admin)]
)


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
