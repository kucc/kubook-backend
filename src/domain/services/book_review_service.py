from datetime import datetime as _datetime
from math import ceil

from fastapi import HTTPException, status
from sqlalchemy import and_, func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload

from domain.schemas.book_review_schemas import (
    DomainReqPostReview,
    DomainReqPutReview,
    DomainResGetReviewByInfoId,
    DomainResGetReviewItem,
    DomainResGetReviewList,
    DomainResGetReviewListByInfoId,
    DomainResPostReview,
)
from repositories.models import Book, BookReview, User
from utils.crud_utils import delete_item, get_item


async def service_read_reviews_by_book_id(
    book_id: int,
    page: int,
    limit: int,
    db: Session
) -> DomainResGetReviewListByInfoId:
    total = db.execute(select(func.count()).select_from(BookReview)
                       .where(and_(BookReview.book_id == book_id, BookReview.is_deleted == False))).scalar()

    if ceil(total/limit) < page:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Page is out of range"
        )
    offset = (page - 1) * limit
    # Using joinedload may reduce queries if the relationships are not large
    stmt = (
        select(BookReview)
        .options(
            joinedload(BookReview.user),
            joinedload(BookReview.book),
        )
        .where(and_(BookReview.book_id == book_id, BookReview.is_deleted == False))
        .order_by(BookReview.updated_at.desc())
        .limit(limit).offset(offset)
    )
    try:
        reviews = db.execute(stmt).scalars().all()
        if not reviews:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reviews not found")

        result = [
            DomainResGetReviewByInfoId(
                review_id=review.id,
                user_id=review.user_id,
                user_name=review.user.user_name,
                book_title=review.book.book_title,
                review_content=review.review_content,
                created_at=review.created_at,
                updated_at=review.updated_at,
            )
            for review in reviews
        ]

        response = DomainResGetReviewListByInfoId(
            data = result,
            total = total
        )

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error occurred during retrieve: {str(e)}",
        ) from e

    return response


async def service_read_reviews_by_user_id(
    user_id: int,
    db: Session
) -> DomainResGetReviewList:
    total = db.execute(select(func.count()).select_from(BookReview)
                       .where(and_(BookReview.user_id == user_id, BookReview.is_deleted == False))).scalar()

    stmt = (
        select(BookReview)
        .where(and_(BookReview.user_id == user_id, BookReview.is_deleted == False))
        .order_by(BookReview.updated_at.desc())
    )

    try:
        reviews = db.scalars(stmt).all()  # loans를 리스트로 반환

        if not reviews:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Reviews not found"
            )

        result = []
        for review in reviews:
            if review.book is None:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Book with ID {review.book_id} not found for review ID {review.id}"
                )
            else:
                result.append(
                    DomainResGetReviewItem(
                        review_id=review.id,
                        user_id=review.user_id,
                        book_id=review.book_id,
                        review_content=review.review_content,
                        created_at=review.created_at,
                        updated_at=review.updated_at,
                        book_title=review.book.book_title,
                    )
                )

        response = DomainResGetReviewList(
            data = result,
            total = total
        )

    except HTTPException as e:
        raise e
    except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected error occurred during retrieve: {str(e)}",
            ) from e

    return response


async def service_delete_review(review_id, user_id, db: Session):
    review = get_item(BookReview, review_id, db)

    if review.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to access this review."
        )

    delete_item(BookReview, review_id, db)
    return


async def service_create_review(request: DomainReqPostReview, db: Session):
    valid_book = get_item(Book, request.book_id, db)

    if not valid_book:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid book info ID")

    review = BookReview(
        user_id=request.user_id,
        book_id=request.book_id,
        review_content=request.review_content,
    )

    try:
        db.add(review)
        db.flush()

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Unexpected error occurred: {str(e)}"
        ) from e

    else:
        db.commit()
        db.refresh(review)

        user = get_item(User, request.user_id, db)
        result = DomainResPostReview(
            review_id=review.id,
            user_id=review.user_id,
            user_name=user.user_name,
            book_id=review.book_id,
            review_content=review.review_content,
            created_at=review.created_at,
        )
    return result


async def service_update_review(request: DomainReqPutReview, db: Session):
    review = get_item(BookReview, request.review_id, db)

    if review.user_id != request.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to access this review."
        )

    try:
        review.review_content = request.review_content
        review.updated_at = _datetime.now()

        db.flush()

    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Integrity Error occurred during update the Review item.: {str(e)}",
        ) from e

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error occurred during update: {str(e)}",
        ) from e

    else:
        db.commit()
        db.refresh(review)

    response = DomainResGetReviewItem(
        review_id=review.id,
        user_id=review.user_id,
        book_id=review.book_id,
        review_content=review.review_content,
        created_at=review.created_at,
        updated_at=review.updated_at,
    )

    return response
