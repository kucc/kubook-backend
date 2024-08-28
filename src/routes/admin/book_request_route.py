from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

import domain.schemas.admin_schemas as s
from dependencies import get_current_admin, get_db
from src.utils.admin_service import *
from repositories.requested_book import RequestedBook

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_current_admin)]
)


@router.get(
    "/book-requests",
    summary="도서 구매 요청 목록 조회",
    response_model=List[s.BookRequestRes],
    status_code=status.HTTP_200_OK
)
async def get_list_book_requests(db: Session = Depends(get_db)):
    return get_list(RequestedBook, db)


@router.get(
    "/book-requests/{request_id}",
    summary="도서 구매 요청 정보 조회",
    response_model=s.BookRequest,
    status_code=status.HTTP_200_OK
)
async def get_book_request(request_id: int, db: Session = Depends(get_db)):
    return get_item(RequestedBook, request_id, db)


@router.patch(
    "/book-requests/{request_id}",
    summary="도서 구매 요청 수정",
    response_model=s.BookRequest,
    status_code=status.HTTP_200_OK
)
async def update_book_request(request_id: int, request_data: BookRequestUpdate, db: Session = Depends(get_db)):
    return update_item(RequestedBook, request_id, request_data, db)


@router.patch(
    "/book-requests/{request_id}/confirm",
    summary="도서 구매 요청 승인 및 거절",
    description='0: 대기, 1: 구매, 2: 신청자 취소 및 삭제(일반 User용), 3: 관리자 반려 및 삭제',
    response_model=s.BookRequestRes,
    status_code=status.HTTP_200_OK
)
async def update_book_request(request_id: int, processing_status: int, reject_reason: str | None, db: Session = Depends(get_db)):
    if processing_status == 1:
        request_data = {
            'processing_status': processing_status
        }
    elif processing_status == 3:
        request_data = {
            'processing_status': processing_status,
            'reject_reason': reject_reason
        }
    else:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail=f"Invalid value range for processing_status. Expected 1(approval) or 3(reject admin), got {processing_status}.")

    return update_item(RequestedBook, request_id, request_data, db)


@router.delete(
    "/book-requests/{request_id}",
    summary="도서 구매 요청 삭제(미개발)",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_book_request(request_id: int, db: Session = Depends(get_db)):
    return delete_item(RequestedBook, request_id, db)
