from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from dependencies import get_current_active_user, get_db

router = APIRouter(
    prefix="/reviews",
    tags=["reviews"]
)


@router.post(
    "/",
    summary="리뷰 작성",
)
async def create_review(db: Session = Depends(get_db), current_user=Depends(get_current_active_user)):
    pass


@router.get(
    "/me",
    summary="내가 작성한 리뷰 목록 조회",
)
async def list_my_reviews(db: Session = Depends(get_db), current_user=Depends(get_current_active_user)):
    pass


@router.get(
    "/books/{book_id}",
    summary="특정 도서에 대한 리뷰 목록 조회",
)
async def list_reviews_of_book(db: Session = Depends(get_db)):
    pass


@router.put(
    "/{review_id}",
    summary="리뷰 수정",
)
async def update_review(db: Session = Depends(get_db), current_user=Depends(get_current_active_user)):
    pass


@router.delete(
    "/{review_id}",
    summary="리뷰 삭제",
)
async def delete_review(db: Session = Depends(get_db), current_user=Depends(get_current_active_user)):
    pass
