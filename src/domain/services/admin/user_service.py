from datetime import datetime, timedelta

from fastapi import HTTPException, status
from sqlalchemy import select, text
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session, selectinload

from domain.schemas.user_schemas import (
    DomainAdminGetUserItem,
    DomainReqAdminDelUser,
    DomainReqAdminPutUser,
    DomainResAdminPutUser,
)
from repositories.models import Admin, User
from utils.crud_utils import delete_item


async def service_admin_search_users(
    user_name: str | None,
    authority: bool | None,
    active: bool | None,
    db: Session
) -> list[DomainAdminGetUserItem]:
    stmt = (
        select(User)
        .options(selectinload(User.admin))
        .where(
                User.is_deleted == False,
        )
    )

    if user_name:
        stmt = (
            stmt.where(text("MATCH(user_name) AGAINST(:user_name IN BOOLEAN MODE)"))
                .params(user_name=f"{user_name}*")
        )
    if authority is not None:
        stmt = stmt.where(User.admin[-1].admin_status == authority)
    if active is not None:
        stmt = stmt.where(User.is_active == active)

    try:
        users = db.execute(stmt.order_by(User.updated_at.desc())).scalars().all()

        if not users:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Users not found")

        search_users = [
            DomainAdminGetUserItem(
                user_id=user.id,
                auth_id=user.auth_id,
                email=user.email,
                user_name=user.user_name,
                github_id=user.github_id,
                instagram_id=user.instagram_id,
                is_active=user.is_active,
                created_at=user.created_at,
                updated_at=user.updated_at,
                is_admin=True if user.admin and user.admin[-1].admin_status else False
            )
            for user in users
        ]

    except HTTPException as e:
            raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error occurred during retrieve: {str(e)}",
        ) from e

    return search_users


async def service_admin_read_users(db: Session) -> list[DomainAdminGetUserItem]:
    stmt = (
        select(User)
        .options(
            selectinload(User.admin)
        )
        .where(
            User.is_deleted == False
        )
    )

    try:
        users = db.execute(stmt.order_by(User.updated_at.desc())).scalars().all()

        if not users:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Users not found")

        search_users = [
            DomainAdminGetUserItem(
                user_id=user.id,
                auth_id=user.auth_id,
                email=user.email,
                user_name=user.user_name,
                github_id=user.github_id,
                instagram_id=user.instagram_id,
                is_active=user.is_active,
                created_at=user.created_at,
                updated_at=user.updated_at,
                is_admin=True if user.admin and user.admin[-1].admin_status else False
            )
            for user in users
        ]

    except HTTPException as e:
            raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error occurred during retrieve: {str(e)}",
        ) from e

    return search_users



async def service_admin_update_user(request: DomainReqAdminPutUser, db: Session):
    user_stmt = select(User).where(User.id == request.user_id, User.is_deleted == False)
    try :
        user = db.execute(user_stmt).scalar_one_or_none()

        if user is None :
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, \
                                detail="Not found user by user_id")

        if request.user_status is not None :
            user.is_active = request.user_status

        if user.admin and not user.admin[-1].is_deleted:
            if request.admin_status == False:
            # 기존 admin이 있고 admin status가 False로 요청된 경우
                user.admin[-1].admin_status = False
                user.admin[-1].is_deleted = True
            if request.expiration_date:
                user.admin[-1].expiration_date = request.expiration_date

        elif request.admin_status:
            # 기존 admin이 없고, 새 admin을 만들어야 하는 경우
            new_admin = Admin(
                user_id=request.user_id,
                admin_status=True,
                expiration_date = request.expiration_date if request.expiration_date \
                else (datetime.today() + timedelta(days=365)).date()  # 1년 후로 만료일 갱신
            )
            db.add(new_admin)

        else:
            # admin 상태 값이 False로 요청되었지만 기존 admin도 없고 새 admin도 생성하지 않는 경우
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not updated admin_status value")

        db.flush()
        db.commit()

    except HTTPException as e:
        raise e

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Unexpected error occurred during update: {str(e)}") from e
    else :
        db.refresh(user)

        response = DomainResAdminPutUser(
                user_id=user.id,
                auth_id=user.auth_id,
                email=user.email,
                user_name=user.user_name,
                is_active=user.is_active,
                is_admin=True if user.admin[-1].admin_status else False,
                expiration_date=user.admin[-1].expiration_date if user.admin[-1].admin_status else None
        )
        return response


async def service_admin_delete_user(request: DomainReqAdminDelUser, db: Session):
    # 유저를 검색해서 관리자가 아니라면 바로 삭제. 관리자라면 관리자 테이블에서 이미 삭제되었는지 확인 후 삭제
    stmt = (
        select(User)
        .where(
            User.id == request.user_id,
            User.is_deleted == False
        )
    )

    try:
        user = db.execute(stmt).scalar_one()

        if user.admin:
            if not user.admin[-1].is_deleted:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Cannot delete an active admin user"
                )
    except NoResultFound as e:
        raise HTTPException(
             status_code=status.HTTP_404_NOT_FOUND,
             detail="User not found"
        ) from e
    except HTTPException as e:
            raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error occurred during user retrieval: {str(e)}",
        ) from e

    delete_item(User, request.user_id, db)

    return
