from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm.session import Session
from datetime import datetime

from repositories.models import Notice, User
from domain.schemas.notice_schemas import DomainResAdminGetNoticeItem, DomainResponseAdminGetNoticeList

async def service_admin_read_notices(page: int, limit: int, db: Session):
    if page < 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="page는 1 이상이어야 합니다.")

    offset=(page-1)*limit

    stmt =(select(Notice)
           .order_by(Notice.created_at)
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
    
    response=[]
    for notice in notices:
        user = db.execute(select(User).where(User.id == notice.admin_id)).scalar()
        admin_name = user.user_name

        response.append(
            DomainResAdminGetNoticeItem(
                notice_id=notice.id,
                admin_id=notice.admin_id,
                admin_name=admin_name,
                title=notice.title,
                notice_content=notice.content,
                created_at=notice.created_at.date()
            )
        )
    response= DomainResponseAdminGetNoticeList(
        data=response, 
        count=len(response))

    return response
