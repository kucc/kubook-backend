from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from dependencies import get_current_admin, get_db
from domain.schemas.notice_schemas import CreateNoticeRequest, NoticeIDRequest, UpdateNoticeRequest
from domain.services.admin.notice_service import (notice_create_sevice,
                                                  notice_delete_service,
                                                  notice_get_item_service,
                                                  notice_get_list_service,
                                                  notice_update_service)
from repositories.models import User
from routes.admin.request.notice_request import NoticeRequest
from routes.admin.response.notice_response import NoticeListResponse, NoticeResponse

router = APIRouter(
    prefix="/admin/notices",
    tags=["admin/notice"],
    dependencies=[Depends(get_db)],
)


@router.get(
    "/",
    response_model=NoticeListResponse,
    status_code=status.HTTP_200_OK,
    summary="전체 공지사항 조회"
)
async def notice_get_list(
    db: Session = Depends(get_db),
):
    data = notice_get_list_service(db)
    # data = [
    #     NoticeResponse(
    #         notice_id=item.notice_id,
    #         title=item.title,
    #         content=item.content,
    #         admin_id=item.admin_id,
    #         author_name=item.author_name  # Get user_name via user_id
    #     )
    #     for item in items
    # ]
    result = NoticeListResponse(
        data=data,
        count=len(data)
    )
    return result


@router.get(
    "/{notice_id}",
    response_model=NoticeResponse,
    status_code=status.HTTP_200_OK,
    summary="특정 ID의 공지사항 조회"
)
async def notice_get_item(
    notice_id: int,
    db: Session = Depends(get_db),
):
    request_domain = NoticeIDRequest(notice_id=notice_id)
    result = notice_get_item_service(request_domain, db)
    return result


@router.post(
    "/",
    response_model=NoticeResponse,
    status_code=status.HTTP_201_CREATED,
    summary="공지사항 추가",
)
async def notice_create_item(
    request: NoticeRequest,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    request_domain = CreateNoticeRequest(
        title=request.title,
        content=request.content,
        admin_id=current_user.admin[0].id,
        user_id=current_user.admin[0].user_id
    )

    result = notice_create_sevice(request_domain, db)
    return result


@router.put(
    "/{notice_id}",
    response_model=NoticeResponse,
    status_code=status.HTTP_200_OK,
    summary="공지사항 수정"
)
async def notice_update_item(
    notice_id: int,
    request: NoticeRequest,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    request_domain = UpdateNoticeRequest(
        notice_id=notice_id,
        title=request.title,
        content=request.content,
        admin_id=current_user.admin[0].id
    )

    result = notice_update_service(request_domain, db)
    return result


@router.delete(
    "/{notice_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="공지사항 삭제"
)
async def notice_delete_item(
    notice_id: int,
    db: Session = Depends(get_db),
):
    request_domain = NoticeIDRequest(notice_id=notice_id)
    notice_delete_service(request_domain, db)
