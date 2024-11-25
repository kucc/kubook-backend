from fastapi import HTTPException, status
from sqlalchemy import select, text
from sqlalchemy.orm import Session, selectinload

from domain.schemas.admin.user_schema import DomainAdminGetUserItem
from repositories.models import User


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
