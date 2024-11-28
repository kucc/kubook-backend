from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from dependencies import get_current_admin, get_db
from domain.schemas.user_schemas import DomainReqAdminPutUser
from domain.services.admin.user_service import service_admin_update_user
from routes.admin.request.user_request import RouteReqAdminPutUser
from routes.admin.response.user_response import RouteResAdminGetUser

router = APIRouter(
    prefix="/admin/users",
    tags=["admin/users"],
    dependencies=[Depends(get_current_admin)]
)

@router.put(
  "/{user_id}",
  summary="관리자의 회원 상태 및 권한 수정",
  status_code=status.HTTP_200_OK,
  response_model=RouteResAdminGetUser
)
async def update_admin_user(
  user_id : int,
  request: RouteReqAdminPutUser,
  db: Session = Depends(get_db),
):
  domain_request = DomainReqAdminPutUser(
    user_id=user_id,
    user_status=request.user_status,
    admin_status=request.admin_status,
    expiration_date=request.expiration_date
  )

  domain_response = await service_admin_update_user(request=domain_request, db=db)

  response = RouteResAdminGetUser(
    user_id=domain_response.user_id,
    auth_id=domain_response.auth_id,
    email=domain_response.email,
    user_name=domain_response.user_name,
    is_active=domain_response.is_active,
    is_admin=domain_response.is_admin,
    expiration_date=domain_response.expiration_date
  )

  return response
