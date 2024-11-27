from fastapi import HTTPException, status
from sqlalchemy import select, text
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session, selectinload

from domain.schemas.user_schemas import DomainAdminGetUserItem, DomainReqAdminDelUser
from repositories.models import User
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
        stmt = stmt.where(User.admin[0].admin_status == authority)
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
                auth_type=user.auth_type,
                email=user.email,
                user_name=user.user_name,
                github_id=user.github_id,
                instagram_id=user.instagram_id,
                is_active=user.is_active,
                created_at=user.created_at,
                updated_at=user.updated_at,
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
                auth_type=user.auth_type,
                email=user.email,
                user_name=user.user_name,
                github_id=user.github_id,
                instagram_id=user.instagram_id,
                is_active=user.is_active,
                created_at=user.created_at,
                updated_at=user.updated_at,
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


async def service_admin_delete_user(request: DomainReqAdminDelUser, db: Session):
    # 유저를 검색해서 관리자가 아니라면 바로 삭제. 관리자라면 관리자 테이블에서 이미 삭제되었는지 확인 후 삭제
    stmt = (
        select(User)
        .options(
            selectinload(User.admin)
        )
        .where(
            User.id == request.user_id,
            User.is_deleted == False
        )
    )

    try:
        user = db.execute(stmt).scalar_one()

        if user.admin:
            if not user.admin[0].is_deleted:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Cannot delete an active admin user"
                )
    except NoResultFound as e:
        raise HTTPException(
             status_code=status.HTTP_404_NOT_FOUND,
             detail="User not found"
        ) from e
    except AttributeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected attribute error occurred: {str(e)}",
        ) from e
    except HTTPException as e:
            raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error occurred during user retrieval: {str(e)}",
        ) from e
    try:
        delete_item(User, request.user_id, db)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error occurred during user deletion: {str(e)}",
        ) from e

    return
