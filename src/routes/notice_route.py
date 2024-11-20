from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session

from dependencies import get_current_active_user, get_db
from domain.services.notice_service import service_read_notices, service_read_notice
from routes.response.notice_response import RouteResGetNotice, RouteResGetNoticeList

router=APIRouter(
    prefix="/notice",
    tags=["notice"],
    dependencies=[Depends(get_current_active_user)]
)

@router.get(
    "",
    response_model=RouteResGetNoticeList,
    status_code=status.HTTP_200_OK,
    summary="공지사항 리스트 전체 조회",
    )

async def get_all_notices(
    page: int = Query(7, ge=1),
    limit: int = Query(10, le=50),
    db: Session=Depends(get_db),
    current_user=Depends(get_current_active_user)
):
    domain_res = await service_read_notices(page, limit, db)
    response = RouteResGetNoticeList(
        data=domain_res,
        count=len(domain_res)
    )

    return response


@router.get(
    "/{notice_id}",
    response_model=RouteResGetNotice,
    status_code=status.HTTP_200_OK,
    summary="공지사항 상세 조회",
    )

async def get_notice(
    notice_id: int,
    db: Session=Depends(get_db),
    current_user=Depends(get_current_active_user)
):
    domain_res = await service_read_notice(notice_id, db)
    response = RouteResGetNotice(
        notice_id=domain_res.notice_id,
        admin_id=domain_res.admin_id,
        admin_name=domain_res.admin_name,
        title=domain_res.title,
        notice_content=domain_res.notice_content,
        created_at=domain_res.created_at
    )

    return response
