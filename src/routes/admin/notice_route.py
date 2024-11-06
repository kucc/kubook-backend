from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session

from dependencies import get_current_admin, get_db
from domain.services.admin.notice_service import service_admin_read_notices
from routes.admin.response.notice_response import RouteResponseAdminGetNoticeItem, RouteResponseAdminGetNoticeList

router=APIRouter(
    prefix="/admin/notice",
    tags=["admin/notice"],
    dependencies=[Depends(get_current_admin)]
)

@router.get(
    "",
    response_model=RouteResponseAdminGetNoticeList,
    status_code=status.HTTP_200_OK,
    summary="공지사항 리스트 조회",
    )

async def get_all_notices(
    page: int = Query(1, gt=0),
    limit: int = Query(10, ge=0),
    db: Session=Depends(get_db),
    current_admin=Depends(get_current_admin)
):
    response = await service_admin_read_notices(page, limit, db)

    return response

