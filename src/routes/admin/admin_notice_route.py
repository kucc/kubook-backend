from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from dependencies import get_current_admin, get_db
from domain.schemas.notice_schemas import DomainReqAdminPostNotice, DomainReqAdminPutNotice
from domain.services.admin.notice_service import (
    service_admin_create_notice,
    service_admin_read_notice,
    service_admin_read_notices,
    service_admin_update_notice,
)
from routes.admin.request.notice_request import RouteReqAdminPostNotice, RouteReqAdminPutNotice
from routes.admin.response.notice_response import (
    RouteResAdminGetNotice,
    RouteResAdminGetNoticeList,
    RouteResAdminPostNotice,
    RouteResAdminPutNotice,
)

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
    page: int = Query(1, ge=1),
    limit: int = Query(7, le=50),
    db: Session=Depends(get_db),
    current_user=Depends(get_current_admin)
):
    domain_res, total = await service_admin_read_notices(page, limit, db)
    response = RouteResAdminGetNoticeList(
        data=domain_res,
        total=total,
        count=len(domain_res)
    )

    return response


@router.get(
    "/{notice_id}",
    response_model=RouteResAdminGetNotice,
    status_code=status.HTTP_200_OK,
    summary="공지사항 상세 조회",
    )

async def get_notice(
    notice_id: int,
    db: Session=Depends(get_db),
    current_user=Depends(get_current_admin)
):
    domain_res = await service_admin_read_notice(notice_id, db)
    response = RouteResAdminGetNotice(
        notice_id=domain_res.notice_id,
        admin_id=domain_res.admin_id,
        admin_name=domain_res.admin_name,
        title=domain_res.title,
        notice_content=domain_res.notice_content,
        created_at=domain_res.created_at
    )

    return response

@router.post(
    "",
    response_model=RouteResAdminPostNotice,
    status_code=status.HTTP_201_CREATED,
    summary="공지사항 등록",
)
async def create_notice(
    notice_create: RouteReqAdminPostNotice,
    db: Session=Depends(get_db),
    current_user=Depends(get_current_admin)
):
    domain_req = DomainReqAdminPostNotice(
        user_id=current_user.id,
        admin_id=current_user.admin[0].id,
        title=notice_create.title,
        notice_content=notice_create.notice_content
    )

    domain_res = await service_admin_create_notice(domain_req, db)
    response = RouteResAdminPostNotice(
        notice_id=domain_res.notice_id,
        admin_name=domain_res.admin_name,
        title=domain_res.title,
        notice_content=domain_res.notice_content,
        created_at=domain_res.created_at
    )

    return response

@router.put(
    "/{notice_id}",
    response_model=RouteResAdminPutNotice,
    status_code=status.HTTP_200_OK,
    summary="공지사항 수정",
)
async def update_notice(
    notice_id: int,
    notice_update: RouteReqAdminPutNotice,
    db: Session=Depends(get_db),
    current_user=Depends(get_current_admin)
):
    domain_req = DomainReqAdminPutNotice(
        notice_id=notice_id,
        admin_id=current_user.admin[0].id,
        title=notice_update.title,
        notice_content=notice_update.notice_content
    )

    domain_res = await service_admin_update_notice(notice_id, domain_req, db)
    response = RouteResAdminPutNotice(
        notice_id=domain_res.notice_id,
        admin_name=domain_res.admin_name,
        title=domain_res.title,
        notice_content=domain_res.notice_content,
        created_at=domain_res.created_at
    )

    return response
