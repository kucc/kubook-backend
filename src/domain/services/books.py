from sqlalchemy.orm import Session
from sqlalchemy import or_, select

from fastapi import HTTPException, status

from datetime import datetime as _datetime

from src.repositories.book import Book
from src.repositories.book_info import BookInfo
from src.repositories.book_category import BookCategory
from src.repositories.book_review import BookReview


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
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Unexpected error occurred during update: {str(e)}")


def submit_book_review(db: Session, current_user, book_info_id: int, content: str):
    try:
        item = db.query(BookInfo).filter(BookInfo.id == book_info_id).first()
        if item == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

        new_review = BookReview(book_indo_id=book_info_id, user_id=current_user, review_content=content)

        db.add(new_review)
        db.commit()
        db.refresh(new_review)

        print(new_review.__dict__)
        return new_review
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Unexpected error occurred during update: {str(e)}")


def update_book_review(db: Session, current_user, index: int, content: str):
    try:
        review = db.query(BookReview).filter(BookReview.id == index).first()
        if review == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")

        if review.user_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this review")

        review.review_content = content
        review.updated_at = _datetime.now()

        db.commit()
        db.refresh(review)

        print(review.__dict__)
        return review
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Unexpected error occurred during update: {str(e)}")


def get_book_review(db: Session, index: int):
    review = select(BookReview).where((BookReview.id == index))
    try:
        result = db.scalar(review)
        if result == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Unexpected error occurred during update: {str(e)}")
