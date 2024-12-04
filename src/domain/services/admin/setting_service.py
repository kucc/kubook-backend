from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm.session import Session

from domain.schemas.setting_schemas import DomainResAdminSetting
from repositories.models import Settings


async def service_admin_read_setting(db: Session):
    #only get the latest setting that is not deleted
    stmt = select(Settings).where(Settings.is_deleted==0).order_by(Settings.created_at.desc()).limit(1)
    setting = db.execute(stmt).scalar_one_or_none()

    if not setting:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Setting not found")

    response = DomainResAdminSetting(
        setting_id=setting.id,
        start_date=setting.start_date.strftime("%Y-%m-%d"),
        end_date=setting.end_date.strftime("%Y-%m-%d"),
        extend_max_count=setting.extend_max_count,
        extend_days=setting.extend_days,
        loan_days=setting.loan_days,
        loan_max_book=setting.loan_max_book,
        request_max_count=setting.request_max_count,
        request_max_price=setting.request_max_price,
        created_at=setting.created_at,
        updated_at=setting.updated_at
    )
    return response
