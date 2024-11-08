from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session

from dependencies import get_current_admin, get_db
from domain.services.admin.notice_service import service_admin_read_notices, service_admin_read_notice
from routes.admin.response.notice_response import RouteResAdminGetNoticeItem, RouteResAdminGetNoticeList

router=APIRouter(
    prefix="/admin/notice",
    tags=["admin/notice"],
    dependencies=[Depends(get_current_admin)]
)

@router.get(
    "",
    response_model=RouteResAdminGetNoticeList,
    status_code=status.HTTP_200_OK,
    summary="공지사항 리스트 전체 조회",
    )

async def get_all_notices(
    page: int = Query(1, gt=0),
    limit: int = Query(10, ge=0),
    db: Session=Depends(get_db),
    current_admin=Depends(get_current_admin)
):
    domain_res = await service_admin_read_notices(page, limit, db)
    response = RouteResAdminGetNoticeList(
        data=domain_res,
        count=len(domain_res)
    )

    return response


@router.get(
    "/{notice_id}",
    response_model=RouteResAdminGetNoticeItem,
    status_code=status.HTTP_200_OK,
    summary="공지사항 상세 조회",
    )

async def get_notice(
    notice_id: int,
    db: Session=Depends(get_db),
    current_admin=Depends(get_current_admin)
):
    domain_res = await service_admin_read_notice(notice_id, db)
    response = RouteResAdminGetNoticeItem(
        notice_id=domain_res.notice_id,
        admin_id=domain_res.admin_id,
        admin_name=domain_res.admin_name,
        title=domain_res.title,
        notice_content=domain_res.notice_content,
        created_at=domain_res.created_at
    )

    return response

