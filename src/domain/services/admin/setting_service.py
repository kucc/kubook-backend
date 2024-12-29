from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm.session import Session

from domain.schemas.setting_schemas import DomainReqAdminSetting, DomainResAdminSetting
from repositories.models import Settings


async def service_admin_read_setting(db: Session):
    #only get the latest setting that is not deleted
    stmt = select(Settings).where(Settings.is_deleted==0).order_by(Settings.updated_at.desc()).limit(1)

    try:
        setting = db.execute(stmt).scalar_one_or_none()
        if not setting:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Setting not found")

        response = DomainResAdminSetting(
            setting_id=setting.id,
            start_date=setting.start_date,
            end_date=setting.end_date,
            extend_max_count=setting.extend_max_count,
            extend_days=setting.extend_days,
            loan_days=setting.loan_days,
            loan_max_book=setting.loan_max_book,
            request_max_count=setting.request_max_count,
            request_max_price=setting.request_max_price,
            created_at=setting.created_at,
            updated_at=setting.updated_at
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error occurred during retrieve: {str(e)}",
        ) from e

    return response

async def service_admin_create_setting(request: DomainReqAdminSetting, db: Session):
    request.set_datetime()
    setting = Settings(
        start_date=request.start_date,
        end_date=request.end_date,
        extend_max_count=request.extend_max_count,
        extend_days=request.extend_days,
        loan_days=request.loan_days,
        loan_max_book=request.loan_max_book,
        request_max_count=request.request_max_count,
        request_max_price=request.request_max_price
    )

    try:
        db.add(setting)
        db.flush()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error occurred during create: {str(e)}",
        ) from e
    else:
        db.commit()
        db.refresh(setting)
        response = DomainResAdminSetting(
            setting_id=setting.id,
            start_date=setting.start_date,
            end_date=setting.end_date,
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
