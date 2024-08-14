from datetime import datetime
from typing import List

from dependencies import get_current_admin, get_current_user, get_db
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from repositories.models import BookInfo, BookStat, LibrarySetting

router = APIRouter(
    prefix="/test",
    tags=["test"]
)


class LibrarySettings(BaseModel):
    id: int
    name: str
    value: str
    data_type: str
    description: str
    created_at: datetime
    updated_at: datetime
    is_valid: bool


@router.get(
    "/library-setting",
    response_model=List[LibrarySettings],
    status_code=status.HTTP_200_OK,
    description="""
    이 API는 get_db로 DB 연결을 테스트하기 위한 API입니다.
    모든 도서관 설정을 조회합니다.
    """,
    summary="모든 도서관 설정 조회",
    response_description={
        200: {"description": "모든 도서관 설정 조회 성공"},
        500: {"description": "서버 에러"}
    }
)
async def get_library_setting(db: Session = Depends(get_db), current_admin: dict = Depends(get_current_user)):
    admin_id = current_admin.id
    library_settings = db.query(LibrarySetting).all()
    return library_settings


class BookStats(BaseModel):
    book_info_id: int
    review_count: int
    loan_count: int
    book_title: str


@router.get(
    "/book-stat",
    response_model=List[BookStats],
    status_code=status.HTTP_200_OK,
    description="""
    이 API는 get_db로 DB 연결을 테스트하기 위한 API입니다.
    모든 도서 통계를 조회합니다.
    """,
    summary="모든 도서 통계 조회",
    response_description={
        200: {"description": "모든 도서 통계 조회 성공"},
        500: {"description": "서버 에러"}
    }
)
async def get_book_stat(db: Session = Depends(get_db)):
    book_stats = db.query(BookStat).all()
    for book_stat in book_stats:
        book_info = db.query(BookInfo).filter(BookInfo.id == book_stat.book_info_id).first()
        book_stat.book_title = book_info.title
    return book_stats


# get_current_user 테스트
@router.get(
    "/current-user",
    status_code=status.HTTP_200_OK,
    description="""
    이 API는 get_current_user로 현재 사용자를 테스트하기 위한 API입니다.
    현재 사용자의 정보를 조회합니다.
    """,
    summary="현재 사용자 정보 조회",
    response_description={
        200: {"description": "현재 사용자 정보 조회 성공"},
        401: {"description": "권한 없음"},
        500: {"description": "서버 에러"}
    }
)
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    return current_user


# get_current_admin 테스트
@router.get(
    "/current-admin",
    status_code=status.HTTP_200_OK,
    description="""
    이 API는 get_current_admin으로 현재 관리자를 테스트하기 위한 API입니다.
    현재 관리자의 정보를 조회합니다.
    """,
    summary="현재 관리자 정보 조회",
    response_description={
        200: {"description": "현재 관리자 정보 조회 성공"},
        401: {"description": "권한 없음"},
        500: {"description": "서버 에러"}
    }
)
async def get_current_admin_info(current_admin: dict = Depends(get_current_admin)):
    return current_admin
