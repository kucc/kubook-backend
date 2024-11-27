from fastapi import HTTPException, status
from sqlalchemy import and_, select
from sqlalchemy.orm.session import Session

from domain.schemas.notice_schemas import DomainResGetNotice
from repositories.models import Notice


async def service_read_notices(page: int, limit: int, db: Session):

    offset=(page-1)*limit

    stmt =(select(Notice)
           .where(Notice.is_deleted == False)
           .order_by(Notice.created_at.desc())
           .limit(limit)
           .offset(offset)
           )

    try:
        notices = db.execute(stmt).scalars().all()
        total=len(db.execute(stmt).scalars().all())
        if total < offset:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Requested page is out of range")
        if not notices:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notices not found")
        elif not total:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Fetch incorrect total value")

        response = [
        DomainResGetNotice(
            notice_id=notice.id,
            admin_id=notice.admin_id,
            admin_name=notice.user.user_name,
            title=notice.title,
            notice_content=notice.content,
            created_at=notice.created_at.date(),
        )
        for notice in notices
    ]
    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error occurred during retrieve: {str(e)}",
        ) from e

    return response, total




async def service_read_notice(notice_id: int, db: Session):
    stmt = select(Notice).where(and_(Notice.id == notice_id, Notice.is_deleted == False))
    notice = db.execute(stmt).scalar()

    if not notice:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notice not found")

    admin_name = notice.user.user_name

    response = DomainResGetNotice(
        notice_id=notice.id,
        admin_id=notice.admin_id,
        admin_name=admin_name,
        title=notice.title,
        notice_content=notice.content,
        created_at=notice.created_at.date()
    )

    return response
