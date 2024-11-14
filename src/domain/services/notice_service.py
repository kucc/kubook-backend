from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm.session import Session

from domain.schemas.notice_schemas import DomainResGetNotice
from repositories.models import Notice


async def service_read_notices(page: int, limit: int, db: Session):
   
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
        DomainResGetNotice(
            notice_id=notice.id,
            admin_id=notice.admin_id,
            admin_name=notice.user[0].user_name,
            title=notice.title,
            notice_content=notice.content,
            created_at=notice.created_at,
        )
        for notice in notices
    ]

    return response




async def service_read_notice(notice_id: int, db: Session):
    stmt = select(Notice).where(Notice.id == notice_id)
    notice = db.execute(stmt).scalar()

    if not notice:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notice not found")

    admin_name = notice.user[0].user_name

    response = DomainResGetNotice(
        notice_id=notice.id,
        admin_id=notice.admin_id,
        admin_name=admin_name,
        title=notice.title,
        notice_content=notice.content,
        created_at=notice.created_at
    )

    return response
