from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from routes.request.update_book_request_request import UpdateBookRequest as route_bookreq_req
from routes.response.book_request_response import BookRequestResponse as route_bookreq_res

from domain.schemas.book_request_schemas import BookRequestRequest as domain_bookreq_req
from domain.services.book_request_service import update as update_bookreq

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
    request_data: route_bookreq_req,
    db: Session = Depends(get_db),
    status_code=status.HTTP_200_OK
):
    domain_req = domain_bookreq_req(
        user_id=user_id,
        request_id=request_id,
        book_title=request_data.book_title,
        publication_year=request_data.publication_year,
        request_link=request_data.request_link,
        reason=request_data.reason,
    )

    domain_res = await update_bookreq(domain_req, db)
    route_res = route_bookreq_res(data=domain_res)
    return route_res
