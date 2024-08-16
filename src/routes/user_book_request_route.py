from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from routes.request.update_book_request_request import UpdateBookRequest as req
from routes.response.book_request_response import BookRequest as res
from dependencies import get_current_active_user, get_db
from domain.services.user_service import *
from repositories.requested_book import RequestedBook

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(get_current_active_user)]
)


@router.put(
    "/{user_id}/book-requests/{requests_id}",
    summary="도서 구매 요청 수정",
    response_model=res,
    status_code=status.HTTP_200_OK
)
async def update_user_book_request(user_id: int, request_id: int, request_data: req, db: Session = Depends(get_db), get_current_active_user=Depends(get_current_active_user)):
    return update_item(RequestedBook, request_id, request_data, db)  # user_service.py 미개발
