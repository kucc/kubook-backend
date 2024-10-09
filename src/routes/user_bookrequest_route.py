from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from dependencies import get_current_active_user, get_db
from domain.schemas.bookrequest_schemas import (ReqeustGetMyBookRequest,
                                                UpdateBookRequestRequest)
from domain.services.bookrequest_service import \
    read_bookrequest as service_read_bookrequest
from domain.services.bookrequest_service import \
    update_bookrequest as service_update_bookrequest
from routes.request.update_bookrequest_request import UpdateBookRequest
from routes.response.bookrequest_response import (BookRequestListResponse,
                                                  BookRequestResponse)

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(get_current_active_user)]
)


@router.get(
    "/{user_id}/book-requests",
    summary="도서 구매 요청 목록 조회",
    response_model=BookRequestListResponse,
    status_code=status.HTTP_200_OK
)
async def get_my_bookrequests(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user)
):
    domain_req = ReqeustGetMyBookRequest(user_id=user_id)
    domain_res = await service_read_bookrequest(domain_req, db)
    converted_res = [BookRequestResponse(
        user_id=item.user_id,
        request_id=item.request_id,
        book_title=item.book_title,
        publication_year=item.publication_year,
        request_link=item.request_link,
        reason=item.reason,
        processing_status=item.processing_status,
        request_date=item.request_date,
        reject_reason=item.reject_reason
    ) for item in domain_res]

    result = BookRequestListResponse(data=converted_res, count=len(converted_res))
    return result


@router.put(
    "/{user_id}/book-requests/{request_id}",
    summary="도서 구매 요청 수정",
    response_model=BookRequestResponse,
    status_code=status.HTTP_200_OK
)
async def update_user_bookrequest(
    user_id: int,
    request_id: int,
    request_data: UpdateBookRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    domain_req = UpdateBookRequestRequest(
        user_id=user_id,
        request_id=request_id,
        book_title=request_data.book_title,
        publication_year=request_data.publication_year,
        request_link=request_data.request_link,
        reason=request_data.reason,
    )

    domain_res = await service_update_bookrequest(domain_req, db)
    result = BookRequestResponse(
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
