from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from dependencies import get_current_active_user, get_db
from domain.schemas.bookrequest_schemas import DomainReqPostBookRequest
from domain.services.bookrequest_service import service_create_bookrequest
from routes.request.bookrequest_request import RouteReqPostBookRequest
from routes.response.bookrequest_response import RouteResPostBookRequest

router = APIRouter(
    prefix="/book-requests",
    tags=["book-requests"],
    dependencies=[Depends(get_current_active_user)]
)


@router.post(
    "",
    response_model=RouteResPostBookRequest,
    status_code=status.HTTP_200_OK,
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
        requested_at=result.requested_at,
        reason=result.reason,
        processing_status=result.processing_status
    )

    return result
