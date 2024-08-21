from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

import domain.schemas.admin_schemas as s
from dependencies import get_current_admin, get_db
from domain.services.admin_service import *
from repositories.models import Book, BookInfo

router = APIRouter(
    prefix="/admin/books",
    tags=["admin/books"],
    dependencies=[Depends(get_current_admin),]
)
# =================== 도서 정보 =========================


@router.get(
    "/book-info",
    summary="도서 정보 목록 조회",
    response_model=List[s.BookInfoRes],
    status_code=status.HTTP_200_OK
)
async def get_list_book_info(db: Session = Depends(get_db)):
    return get_list(BookInfo, db)


@router.get(
    "/book-info/{book_info_id}",
    summary="도서 정보 조회",
    response_model=s.BookInfo,
    status_code=status.HTTP_200_OK
)
async def get_book_info(book_info_id: int, db: Session = Depends(get_db)):
    return get_item(BookInfo, book_info_id, db)


@router.post(
    "/book-info",
    summary="도서 정보 등록",
    response_model=s.BookInfo,
    status_code=status.HTTP_201_CREATED
)
async def create_book_info(book_info_data: s.BookInfoCreate, db: Session = Depends(get_db)):
    return create_item(BookInfo, book_info_data, db)


@router.patch(
    "/book-info/{book_info_id}",
    summary="도서 정보 수정",
    response_model=s.BookInfo,
    status_code=status.HTTP_200_OK
)
async def update_book_info(book_info_id: int, book_info_data: s.BookInfoCreate, db: Session = Depends(get_db)):
    return update_item(BookInfo, book_info_id, book_info_data, db)


@router.delete(
    "/book-info/{book_info_id}",
    summary="도서 정보 삭제",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_book_info(book_info_id: int, db: Session = Depends(get_db)):
    return delete_item(BookInfo, book_info_id, db)

# =================== 책 정보 =========================


@router.get(
    "/books",
    summary="책 정보 목록 조회",
    response_model=List[s.BookRes],
    status_code=status.HTTP_200_OK
)
async def get_list_books(db: Session = Depends(get_db)):
    return get_list(Book, db)


@router.get(
    "/books/{book_id}",
    summary="책 정보 조회",
    response_model=s.Book,
    status_code=status.HTTP_200_OK
)
async def get_book_info(book_id: int, db: Session = Depends(get_db)):
    return get_item(Book, book_id, db)


# @router.post(
#     "/books",
#     summary="책 정보 등록",
#     response_model=s.Book,
#     status_code=status.HTTP_201_CREATED
# )
# async def create_book(book_data: BookCreate, db: Session = Depends(get_db)):
#     return create_item(Book, book_data, db)


# @router.patch(
#     "/books/{book_id}",
#     summary="책 정보 수정",
#     response_model=s.Book,
#     status_code=status.HTTP_200_OK
# )
# async def update_book(book_id: int, book_data: BookUpdate, db: Session = Depends(get_db)):
#     return update_item(Book, book_id, book_data, db)


@router.delete(
    "/books/{book_id}",
    summary="책 정보 삭제",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_book(book_id: int, current_user: User = Depends(get_current_admin), db: Session = Depends(get_db)):
    return delete_item(Book, book_id, db)
