from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm.session import Session

from domain.schemas.notice_schemas import (
    DomainReqAdminPostNotice,
    DomainReqAdminPutNotice,
    DomainResAdminGetNotice,
    DomainResAdminPostNotice,
    DomainResAdminPutNotice,
)
from repositories.models import Notice


async def service_admin_read_notices(page: int, limit: int, db: Session):

    offset=(page-1)*limit

    stmt =(select(Notice)
           .order_by(Notice.created_at.desc())
           .limit(limit)
           .offset(offset)
           )

    try:
        notices = db.execute(stmt).scalars().all()
        if not notices:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notices not found")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error occurred during retrieve: {str(e)}",
        ) from e


    response = [
        DomainResAdminGetNotice(
            notice_id=notice.id,
            admin_id=notice.admin_id,
            admin_name=notice.user.user_name,
            title=notice.title,
            notice_content=notice.content,
            created_at=notice.created_at.date(),
        )
        for notice in notices
    ]

    return response




async def service_admin_read_notice(notice_id: int, db: Session):
    stmt = select(Notice).where(Notice.id == notice_id)
    notice = db.execute(stmt).scalar()

    if not notice:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notice not found")

    admin_name = notice.user.user_name

    response = DomainResAdminGetNotice(
        notice_id=notice.id,
        admin_id=notice.admin_id,
        admin_name=admin_name,
        title=notice.title,
        notice_content=notice.content,
        created_at=notice.created_at.date(),
    )

    return response




async def service_admin_create_notice(request: DomainReqAdminPostNotice, db: Session):

    if not request.title.strip() or not request.notice_content.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="title or notice_content is empty")

    notice = Notice(
        user_id=request.user_id,
        admin_id=request.admin_id,
        title=request.title,
        content=request.notice_content
    )
    try:
        db.add(notice)
        db.flush()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Unexpected error occurred: {str(e)}"
        ) from e

    else:
        db.commit()
        db.refresh(notice)

        result = DomainResAdminPostNotice(
            notice_id=notice.id,
            admin_name=notice.user.user_name,
            title=notice.title,
            notice_content=notice.content,
            created_at=notice.created_at.date(),
        )
    return result


async def service_admin_update_notice(notice_id: int, request: DomainReqAdminPutNotice, db: Session):
    stmt = select(Notice).where(Notice.id == notice_id)
    notice = db.execute(stmt).scalar_one_or_none()

    if not notice:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Notice not found")

    try:
        notice.title = request.title
        notice.content = request.notice_content
        db.add(notice)
        db.flush()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Unexpected error occurred: {str(e)}"
        ) from e
    else:
        db.commit()
        db.refresh(notice)

        domain_res = DomainResAdminPutNotice(
            notice_id=notice.id,
            title=notice.title,
            notice_content=notice.content,
            admin_name=notice.user.user_name,
            created_at=notice.created_at.date(),
        )
    return domain_res

