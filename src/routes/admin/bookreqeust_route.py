from fastapi import APIRouter, Depends, Query, status
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
  db: Session = Depends(get_db),
  page: int = Query(1, gt=0),
  limit: int = Query(10, gt=0),
):
    domain_result = await service_admin_read_bookreqeust(db=db, page=page, limit=limit)
    result = RouteResAdminGetBookReqeustList(
      data=domain_result.data,
      count=domain_result.count
    )
    return result
