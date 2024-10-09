from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from dependencies import get_current_active_user, get_db
from domain.schemas.bookrequest_schemas import DomainReqDelBookRequest, DomainReqGetBookRequest, DomainReqPutBookRequest
from domain.services.bookrequest_service import (
    service_delete_bookrequest,
    service_read_bookrequest,
    service_update_bookrequest,
)
from routes.request.bookrequest_request import RouteReqPutBookRequest
from routes.response.bookrequest_response import RouteResBookRequest, RouteResBookRequestList

router = APIRouter(dependencies=[Depends(get_current_active_user)])


@router.get(
    "/users/{user_id}/book-requests",
    tags=["users"],
    summary="도서 구매 요청 목록 조회",
    response_model=RouteResBookRequestList,
    status_code=status.HTTP_200_OK,
)
async def get_user_bookrequests(
    user_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_active_user)
):
    domain_req = DomainReqGetBookRequest(user_id=user_id)
    domain_res = await service_read_bookrequest(domain_req, db)
    converted_res = [
        RouteResBookRequest(
            user_id=item.user_id,
            request_id=item.request_id,
            book_title=item.book_title,
            publication_year=item.publication_year,
            request_link=item.request_link,
            reason=item.reason,
            processing_status=item.processing_status,
            request_date=item.request_date,
            reject_reason=item.reject_reason,
        )
        for item in domain_res
    ]

    result = RouteResBookRequestList(data=converted_res, count=len(converted_res))
    return result


@router.put(
    "/users/{user_id}/book-requests/{request_id}",
    tags=["users"],
    summary="도서 구매 요청 수정",
    response_model=RouteResBookRequest,
    status_code=status.HTTP_200_OK,
)
async def update_user_bookrequest(
    user_id: int,
    request_id: int,
    request_data: RouteReqPutBookRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    domain_req = DomainReqPutBookRequest(
        user_id=user_id,
        request_id=request_id,
        book_title=request_data.book_title,
        publication_year=request_data.publication_year,
        request_link=request_data.request_link,
        reason=request_data.reason,
    )

    domain_res = await service_update_bookrequest(domain_req, db)
    result = RouteResBookRequest(
        user_id=domain_res.user_id,
        request_id=domain_res.request_id,
        book_title=domain_res.book_title,
        publication_year=domain_res.publication_year,
        request_link=domain_res.request_link,
        reason=domain_res.reason,
        processing_status=domain_res.processing_status,
        request_date=domain_res.request_date,
        reject_reason=domain_res.reject_reason,
    )
    return result


@router.delete(
    "/book-requests/{request_id}",
    tags=["book-requests"],
    summary="도서 구매 요청 삭제 (요청자 취소)",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user_bookrequest(
    request_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_active_user)
) -> None:
    domain_req = DomainReqDelBookRequest(user_id=current_user.id, request_id=request_id)
    await service_delete_bookrequest(domain_req, db)

    return
