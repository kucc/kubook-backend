from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from dependencies import get_current_admin, get_db
from domain.services.admin.setting_service import service_admin_read_setting
from routes.admin.response.setting_response import (
    BookRequestSetting,
    ExtendSetting,
    LoanSetting,
    RouteResAdminSetting,
    ServiceDate,
)

router = APIRouter(
    prefix="/admin/setting",
    tags=["admin/setting"],
    dependencies=[Depends(get_current_admin)]
)

@router.get(
    "",
    response_model=RouteResAdminSetting,
    summary="설정 조회",
)
async def get_setting(
    db: Session = Depends(get_db),
):
    domain_res = await service_admin_read_setting(db)


    service_date = ServiceDate(start_date=domain_res.start_date, end_date=domain_res.end_date)
    loan = LoanSetting(loan_days=domain_res.loan_days, loan_max_book=domain_res.loan_max_book)
    extend = ExtendSetting(extend_days=domain_res.extend_days, extend_max_count=domain_res.extend_max_count)
    bookrequest = BookRequestSetting(
        request_max_count=domain_res.request_max_count,
        request_max_price=domain_res.request_max_price
    )

    response = RouteResAdminSetting(
        setting_id=domain_res.setting_id,
        service_date=service_date,
        loan=loan,
        extend=extend,
        bookrequest=bookrequest,
        created_at=domain_res.created_at,
        updated_at=domain_res.updated_at

    )
    return response
