from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from routes.request.update_book_request_request import UpdateBookRequest as route_update_bookreq_req
from routes.response.book_request_response import BookRequestResponse as route_bookreq_res

from domain.schemas.book_request_schemas import BookRequestUpdateRequest as domain_update_bookreq_req
from domain.services.book_request_service import update

from dependencies import get_current_active_user, get_db
# from repositories.requested_book import RequestedBook

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(get_current_active_user)]
)


@router.put(
    "/{user_id}/book-requests/{requests_id}",
    summary="도서 구매 요청 수정",
    response_model=route_bookreq_res,
    status_code=status.HTTP_200_OK
)
async def update_user_book_request(
    user_id: int,
    request_id: int,
    request_data: route_update_bookreq_req,
    db: Session = Depends(get_db),
    get_current_active_user=Depends(get_current_active_user)
):
    domain_req = domain_update_bookreq_req(
        user_id=user_id,
        id=request_id,
        book_title=request_data.book_title,
        publication_year=request_data.publication_year,
        request_link=request_data.request_link,
        reason=request_data.reason,
    )

    return await update(domain_req, db)
