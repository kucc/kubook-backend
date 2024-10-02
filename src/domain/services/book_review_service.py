from fastapi import HTTPException, status
from sqlalchemy import and_, select
from sqlalchemy.orm import Session, selectinload

from domain.schemas.book_review_schemas import (
    DomainReqPostReview,
    DomainReqPutReview,
    DomainResGetReviewByInfoId,
    DomainResGetReviewItem,
    DomainResPostReview,
)
from repositories.models import BookReview, User
from utils.crud_utils import create_item, delete_item, get_item, update_item


async def service_read_reviews_by_bookinfo_id(book_info_id, db: Session):
    stmt = (
        select(BookReview)
        .options(selectinload(BookReview.user))
        .where(
            and_(
                BookReview.book_info_id == book_info_id,
                BookReview.is_deleted == False
            )
        )
        .order_by(BookReview.updated_at)
    )
    try:
        reviews = db.execute(stmt).scalars().all()

        if not reviews:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Reviews not found"
            )

        response = [
            DomainResGetReviewByInfoId(
                review_id=review.id,
                user_id=review.user_id,
                user_name=review.user.user_name,
                review_content=review.review_content,
                created_at=review.created_at,
                updated_at=review.updated_at
            )
            for review in reviews
        ]

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error occurred during retrieve: {str(e)}"
            ) from e

    return response



async def service_read_reviews_by_user_id(user_id, db: Session):
    stmt = (
        select(BookReview)
        .where(
            and_(
                BookReview.user_id == user_id,
                BookReview.is_deleted == False
            )
        )
        .order_by(BookReview.updated_at))

    try:
        reviews = db.scalars(stmt).all()  # loans를 리스트로 반환
        if not reviews:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Reviews not found")

        result = [
            DomainResGetReviewItem(
                review_id=review.id,
                user_id=review.user_id,
                book_info_id=review.book_info_id,
                review_content=review.review_content,
                created_at=review.created_at,
                updated_at=review.updated_at
            )
            for review in reviews
        ]

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error occurred during retrieve: {str(e)}"
            ) from e
    return result


async def service_delete_review(review_id, user_id, db: Session):
    review = get_item(BookReview, review_id, db)

    if review.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this review."
            )

    delete_item(BookReview, review_id, db)
    return


async def service_create_review(request: DomainReqPostReview, db: Session):
    valid_book_info = get_item(BookReview, request.book_info_id, db)

    if not valid_book_info:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid book info ID"
            )

    review = BookReview(
        user_id=request.user_id,
        book_info_id=request.book_info_id,
        review_content=request.review_content,
    )

    created_review = create_item(BookReview, review, db)

    user = get_item(User, request.user_id, db)
    result = DomainResPostReview(
        review_id=created_review.id,
        user_id=created_review.user_id,
        user_name=user.user_name,
        book_info_id=created_review.book_info_id,
        review_content=created_review.review_content,
        created_at=created_review.created_at,
    )
    return result


async def service_update_review(request: DomainReqPutReview, db: Session):
    review = get_item(BookReview, request.review_id, db)

    if review.user_id != request.user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="You do not have permission to access this review.")

    review.review_content = request.review_content
    dict = {"review_content": review.review_content}

    updated_review = update_item(BookReview, request.review_id, dict, db)


    response = DomainResGetReviewItem(
        review_id=updated_review.id,
        user_id=updated_review.user_id,
        book_info_id=updated_review.book_info_id,
        review_content=updated_review.review_content,
        created_at=updated_review.created_at,
        updated_at=updated_review.updated_at
    )

    return response

