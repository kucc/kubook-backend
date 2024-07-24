from sqlalchemy.orm import Session
from sqlalchemy import or_, select

from fastapi import HTTPException, status

from src.repositories.book import Book
from src.repositories.book_info import BookInfo
from src.repositories.book_category import BookCategory
from src.domain.schemas.books import models, schemas


def search_books(db: Session, search_query: str):
    try:
        results = db.query(BookInfo).filter(
            or_(
                BookInfo.title.ilike(f"%{search_query}"),
                BookInfo.author.ilike(f"%{search_query}"),
                # BookInfo.isbn.ilike(f"%{search_query}"),
                # db, 모델, 스키마 모두에 isbn 항목이 없어서 보류.
            )
        ).all()
        if results == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Unexpected error occurred during update: {str(e)}")

    return results


def get_books_by_category(db: Session, category_id: int):
    pass


def get_book_detail(db: Session, index: int):
    stmt = select(BookInfo).where((BookInfo.id == index))
    try:
        result = db.scalar(stmt)
        if result == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Unexpected error occurred during update: {str(e)}")

    return result


def submit_book_review(db: Session, ):
    pass
