from fastapi import HTTPException, status
from sqlalchemy import and_, func, select
from sqlalchemy.orm.session import Session

from domain.schemas.notice_schemas import DomainResGetNotice
from repositories.models import Notice


async def service_read_notices(page: int, limit: int, db: Session):

    offset=(page-1)*limit

    count_stmt=select(Notice).where(Notice.is_deleted == False)
    total_stmt=count_stmt.with_only_columns(func.count(Notice.id))
    stmt = count_stmt.order_by(Notice.created_at.desc()).limit(limit).offset(offset)

    try:
        total=db.execute(total_stmt).scalar()
        if total < page*limit:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Requested page is out of range")

        notices = db.execute(stmt).scalars().all()
        if not notices:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notices not found")

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
