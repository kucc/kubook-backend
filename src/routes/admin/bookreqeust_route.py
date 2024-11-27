from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from dependencies import get_current_admin, get_db
from domain.services.admin.bookreqeust_service import service_admin_read_bookreqeust
from routes.admin.response.bookrequest_response import RouteResAdminGetBookReqeustList

router = APIRouter(
    prefix="/admin/book-requests",
    tags=["admin/book-requests"],
    dependencies=[Depends(get_current_admin)]
)

@router.get(
  "",
  response_model= RouteResAdminGetBookReqeustList,
  status_code = status.HTTP_200_OK,
  summary="관리자 도서 구매 요청 목록 조회"
)
async def admin_read_bookreqeust(
  db: Session = Depends(get_db)
):
    domain_result = await service_admin_read_bookreqeust(db)
    result = RouteResAdminGetBookReqeustList(
      data=domain_result,
      count=len(domain_result)
    )
    return result
