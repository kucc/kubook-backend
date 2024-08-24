from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from dependencies import get_current_active_user, get_db

router = APIRouter(
    prefix="/book-requests",
    tags=["book-requests"]
)


@router.post(
    "/",
    summary="도서 구매 요청 생성",
)
async def create_book_request(db: Session = Depends(get_db), get_current_active_user=Depends(get_current_active_user)):
    pass
