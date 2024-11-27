from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from dependencies import get_current_admin, get_db
from domain.schemas.bookrequest_schemas import DomainReqAdminPutBookRequest
from domain.services.admin.bookreqeust_service import service_admin_read_bookreqeust, service_admin_update_bookrequest
from routes.admin.response.bookrequest_response import RouteResAdminGetBookReqeustList, RouteResAdminPutBookReqeust

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

@router.put(
  "/{request_id}",
  response_model=RouteResAdminPutBookReqeust,
  summary="관리자 도서 구매 요청 상태 수정"
)
async def admin_update_bookrequest(
  db: Session,
  reqeust_id: int,
  processing_status: int,
  reason: str | None
):
    domain_req = DomainReqAdminPutBookRequest(
      reqeust_id = reqeust_id,
      processing_status = processing_status,
      reason = reason
    )
    domain_res = await service_admin_update_bookrequest(db=db, request=domain_req)
    result = RouteResAdminPutBookReqeust(
      user_id=domain_res.user_id,
      reqeust_id=domain_res.reqeust_id,
      book_title=domain_res.book_title,
      publication_year=domain_res.publication_year,
      request_link=domain_res.request_link,
      reason=domain_res.reason,
      processing_status=domain_res.processing_status,
      request_date=domain_res.request_date,
      reject_reason=domain_res.reject_reason
    )
    return result
