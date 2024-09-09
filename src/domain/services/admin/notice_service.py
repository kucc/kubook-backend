from typing import List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from repositories.models import Notice
from domain.schemas.notice_schemas import NoticeIDRequest, CreateNoticeRequest, UpdateNoticeRequest, NoticeResponse
from utils.crud_utils import get_list, get_item, create_item, update_item, delete_item


def notice_get_list_service(db: Session) -> List[NoticeResponse]:
    # Fetch items from the database
    items = get_list(Notice, db)  
    # Map the items to the NoticeResponse model
    result = [
        NoticeResponse(
            notice_id=item.id,
            title=item.title,
            content=item.content,
            admin_id=item.admin_id,
            author_name=item.user.user_name  # Get user_name via user_id
        )
        for item in items
    ]
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No items found"
        )
    if any(not isinstance(item, NoticeResponse) for item in result):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Service return type error: returned result does not match expected return type."
        )
    return result



def notice_get_item_service(request: NoticeIDRequest, db: Session) -> NoticeResponse:
    item = get_item(Notice, request.notice_id, db)
    result = NoticeResponse(
        notice_id=item.id,
        title=item.title,
        content=item.content,
        admin_id=item.admin_id,
        author_name=item.user.user_name  # user_id를 통해 user_name 가져오기
    )
    if not isinstance(result, NoticeResponse):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Service return type error: returned result does not match expected return type.")
    return result


def notice_create_sevice(request: CreateNoticeRequest, db: Session) -> NoticeResponse:
    item = create_item(Notice, request, db)
    result = NoticeResponse(
        notice_id=item.id,
        title=item.title,
        content=item.content,
        admin_id=item.admin_id,
        author_name=item.user.user_name  # user_id를 통해 user_name 가져오기
    )
    if not isinstance(result, NoticeResponse):
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Service return type error: returned result does not match expected return type.")
    db.commit()
    return result


def notice_update_service(reqeust: UpdateNoticeRequest, db: Session) -> NoticeResponse:
    item = update_item(Notice, reqeust.notice_id, reqeust, db)

    result = NoticeResponse(
        notice_id=item.id,
        title=item.title,
        content=item.content,
        admin_id=item.admin_id,
        author_name=item.user.user_name  # user_id를 통해 user_name 가져오기
    )
    if not isinstance(result, NoticeResponse):
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Service return type error: returned result does not match expected return type.")
    db.commit()
    return result


def notice_delete_service(request: NoticeIDRequest, db: Session):
    delete_item(Notice, request.notice_id, db)
