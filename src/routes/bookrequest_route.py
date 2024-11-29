from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from dependencies import get_current_active_user, get_db
from domain.schemas.bookrequest_schemas import (
    DomainReqDelBookRequest,
    DomainReqPostBookRequest,
    DomainReqPutBookRequest,
)
from domain.services.bookrequest_service import (
    service_create_bookrequest,
    service_delete_bookrequest,
    service_update_bookrequest,
)
from routes.request.bookrequest_request import RouteReqPostBookRequest, RouteReqPutBookRequest
from routes.response.bookrequest_response import RouteResBookRequest, RouteResPostBookRequest

router = APIRouter(
    prefix="/book-requests",
    tags=["book-requests"],
    dependencies=[Depends(get_current_active_user)]
)

@router.post(
    "",
    response_model=RouteResPostBookRequest,
    status_code=status.HTTP_201_CREATED,
    summary="구매 요청"
)
async def create_book_request(
    purchase_create: RouteReqPostBookRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user)
):
    domain_req = DomainReqPostBookRequest(
        user_id=current_user.id,
        book_title=purchase_create.book_title,
        publication_year=purchase_create.publication_year,
        request_link=purchase_create.request_link,
        reason=purchase_create.reason
    )

    result = await service_create_bookrequest(domain_req, db)

    result = RouteResPostBookRequest(
        request_id=result.request_id,
        user_id=result.user_id,
        book_title=result.book_title,
        publication_year=result.publication_year,
        request_link=result.request_link,
        request_date=result.request_date,
        reason=result.reason,
        processing_status=result.processing_status
    )

    return result


@router.put(
    "/{request_id}",
    summary="user의 도서 구매 요청 수정",
    response_model=RouteResBookRequest,
    status_code=status.HTTP_200_OK,
)
async def update_user_bookrequest(
    request_id: int,
    request_data: RouteReqPutBookRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    domain_req = DomainReqPutBookRequest(
        user_id=current_user.id,
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
    "/{request_id}",
    summary="도서 구매 요청 삭제 (요청자 취소)",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user_bookrequest(
    request_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_active_user)
) -> None:
    domain_req = DomainReqDelBookRequest(user_id=current_user.id, request_id=request_id)
    await service_delete_bookrequest(domain_req, db)

    return
