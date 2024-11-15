from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from repositories.models import User
from routes.admin.response.user_response import RouteAdminsGetUserItem, RouteResAdminGetUserList


async def service_admin_search_users(
        user_name: str,
        authority: bool,
        active: bool,
        db: Session
):
    keyword = f"%{user_name}%"

    stmt = (
        select(User)
        .options(selectinload(User.admin))
        .where(
                User.is_deleted == False,
        )
    )

    if user_name:
        stmt = stmt.where(User.user_name.ilike(keyword))
    if authority is not None:
        stmt = stmt.where(User.admin[0].admin_status == authority)
    if active is not None:
        stmt = stmt.where(User.is_active == active)

    try:
        users = db.execute(stmt.order_by(User.updated_at.desc())).scalars().all()

        if not users:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Users not found")

        search_users = [
            RouteAdminsGetUserItem(
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

        response = RouteResAdminGetUserList(
            data=search_users,
            count=len(search_users)
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error occurred during retrieve: {str(e)}",
        ) from e

    return response
