from datetime import datetime, timedelta

from fastapi import HTTPException, status
from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from domain.schemas.user_schemas import DomainReqAdminPutUser, DomainResAdminPutUser
from repositories.models import Admin, User


# 서비스 함수
async def service_admin_update_user(request: DomainReqAdminPutUser, db: Session):

    if request.user_status is not None :
        user_stmt = select(User).where(User.id == request.user_id, User.is_deleted == False)
        try :
            user = db.execute(user_stmt).scalar_one()
            if user :
                user.is_active = request.user_status

            db.flush()
            db.commit()

        except Exception as e:
            if not isinstance(e, HTTPException):
                db.rollback()
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail=f"Unexpected error occurred during update: {str(e)}") from e
        else :
            db.refresh(user)



    stmt = select(Admin).where(and_(Admin.user_id == request.user_id,
                        Admin.admin_status == True,
                        Admin.is_deleted == False))
    try:
        # 기존 admin 조회
        admin = db.execute(stmt).scalar_one_or_none()
        if admin :
            if request.admin_status == False:
            # 기존 admin이 있고 admin status가 False로 요청된 경우
                admin.admin_status = False
                admin.is_deleted = True
            if request.expiration_date:
                admin.expiration_date = request.expiration_date

        elif request.admin_status:
            # 기존 admin이 없고, 새 admin을 만들어야 하는 경우
            new_admin = Admin(
                user_id=request.user_id,
                admin_status=True,
                expiration_date = request.expiration_date if request.expiration_date \
                else (datetime.today() + timedelta(days=365)).date()  # 1년 후로 만료일 갱신
            )
            db.add(new_admin)
            admin = new_admin  # 새로 추가된 admin을 admin 변수에 할당

        else:
            # admin 상태 값이 False로 요청되었지만 기존 admin도 없고 새 admin도 생성하지 않는 경우
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not updated admin_status value")

        # DB에 변경사항 반영
        db.flush()
        db.commit()

    except Exception as e:
        db.rollback()
        if not isinstance(e, HTTPException):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected error occurred during update: {str(e)}",
            ) from e
    else :
        db.refresh(admin)

    # admin 값이 존재하면 이를 갱신 후, DomainResAdminGetUser로 변환하여 응답
    if admin:
        # DomainResAdminGetUser에 값을 담아서 응답
        response = DomainResAdminPutUser(
            user_id=admin.user_id,
            auth_id=admin.user.auth_id,
            email=admin.user.email,
            user_name=admin.user.user_name,
            is_active=admin.user.is_active,
            is_admin=admin.admin_status,
            expiration_date=admin.expiration_date
        )

    else :
        response = DomainResAdminPutUser(
            user_id=user.id,
            auth_id=user.auth_id,
            email=user.email,
            user_name=user.user_name,
            is_active=user.is_active,
            is_admin=True if user.admin[0].admin_status else False,
            expiration_date=user.admin[0].expiration_date if user.admin[0].admin_status else None
        )

    return response



