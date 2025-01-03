from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from dependencies import get_current_admin, get_db
from domain.schemas.bookrequest_schemas import DomainReqAdminPutBookRequest
from domain.services.admin.bookrequest_service import (
    service_admin_delete_bookrequest,
    service_admin_read_bookrequest,
    service_admin_update_bookrequest,
)
from routes.admin.request.bookrequest_request import RouteReqAdminPutBookRequest
from routes.admin.response.bookrequest_response import RouteResAdminGetBookRequestList, RouteResAdminPutBookRequest

router = APIRouter(
    prefix="/admin/book-requests",
    tags=["admin/book-requests"],
    dependencies=[Depends(get_current_admin)]
)

@router.get(
  "",
  response_model= RouteResAdminGetBookRequestList,
  status_code = status.HTTP_200_OK,
  summary="관리자 도서 구매 요청 목록 조회"
)
async def admin_read_bookRequest(
  db: Session = Depends(get_db),
  page: int = Query(1, gt=0),
  limit: int = Query(10, gt=0),
):
    domain_result = await service_admin_read_bookrequest(db=db, page=page, limit=limit)
    result = RouteResAdminGetBookRequestList(
      data=domain_result.data,
      count=len(domain_result.data),
      total=domain_result.total
    )
    return result

@router.put(
  "/{request_id}",
  response_model=RouteResAdminPutBookRequest,
  status_code=status.HTTP_200_OK,
  summary="관리자 도서 구매 요청 상태 수정"
)
async def admin_update_bookrequest(
  request_id: int,
  request: RouteReqAdminPutBookRequest,
  db: Session = Depends(get_db)
):
    domain_req = DomainReqAdminPutBookRequest(
      request_id = request_id,
      processing_status = request.processing_status,
      reject_reason = request.reject_reason
    )
    domain_res = await service_admin_update_bookrequest(db=db, request=domain_req)
    result = RouteResAdminPutBookRequest(
      user_id=domain_res.user_id,
      request_id=domain_res.request_id,
      book_title=domain_res.book_title,
      publication_year=domain_res.publication_year,
      request_link=domain_res.request_link,
      reason=domain_res.reason,
      processing_status=domain_res.processing_status,
      request_date=domain_res.request_date,
      reject_reason=domain_res.reject_reason
    )
    return result

@router.delete(
  "/{request_id}",
  status_code=status.HTTP_204_NO_CONTENT,
  summary="관리자 도서 구매 요청 삭제"
)
async def admin_delete_bookrequest(
  request_id: int,
  db: Session = Depends(get_db)
):
    await service_admin_delete_bookrequest(request_id=request_id, db=db)
    return
