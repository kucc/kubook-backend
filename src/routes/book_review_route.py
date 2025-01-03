from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from dependencies import get_current_user, get_db
from domain.schemas.book_review_schemas import (
    DomainReqPostReview,
    DomainReqPutReview,
    DomainResGetReviewItem,
    DomainResPostReview,
)
from domain.services.book_review_service import (
    service_create_review,
    service_delete_review,
    service_read_reviews_by_book_id,
    service_update_review,
)
from routes.request.book_review_request import RouteReqPostReview, RouteReqPutReview
from routes.response.book_review_response import RouteResGetReviewListByInfoId

router = APIRouter(
    prefix="/reviews",
    tags=["reviews"],
)


@router.get(
    "/",
    response_model=RouteResGetReviewListByInfoId,
    status_code=status.HTTP_200_OK,
    summary="책에 대한 리뷰 조회"
)
async def get_all_reviews_by_book_id(
    book_id: int = Query(alias="books"),
    page: int =  Query(1, gt=0),
    limit: int = Query(10, gt=0),
    db: Session = Depends(get_db),
):
    domain_res = await service_read_reviews_by_book_id(book_id=book_id, page=page, limit=limit, db=db)

    result = RouteResGetReviewListByInfoId(
        data=domain_res.data,
        count=len(domain_res.data), # count는 현재 page에 있는 리뷰의 개수
        total=domain_res.total # total은 총 리뷰의 개수
    )

    return result


@router.post(
    "",
    response_model=DomainResPostReview,
    status_code=status.HTTP_201_CREATED,
    summary="리뷰 작성",
    dependencies=[Depends(get_current_user)]
)
async def create_review(
    route_req: RouteReqPostReview,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    domain_req = DomainReqPostReview(
        user_id=current_user.id,
        book_id=route_req.book_id,
        review_content=route_req.review_content
    )
    result = await service_create_review(domain_req, db)
    return result


@router.delete(
    "/{review_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="리뷰 삭제",
    dependencies=[Depends(get_current_user)]
)
async def delete_reivew(
    review_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    await service_delete_review(review_id, current_user.id, db)
    return

@router.put(
    "/{review_id}",
    response_model=DomainResGetReviewItem,
    status_code=status.HTTP_200_OK,
    summary="리뷰 수정",
    dependencies=[Depends(get_current_user)]
)
async def update_review(
    review_id: int,
    review_update_data: RouteReqPutReview,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    domain_req = DomainReqPutReview(
        review_id=review_id,
        review_content=review_update_data.review_content,
        user_id=current_user.id
    )
    result = await service_update_review(domain_req, db)
    return result

