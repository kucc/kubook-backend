from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from domain.schemas.user_schemas import DomainResGetUser, DomainReqPutUser, DomainResPutUser
from repositories.models import User
from utils.crud_utils import get_item

async def service_read_user(user_id:int, db: Session):
    user = get_item(User, user_id, db)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Requested user not found")

    response = DomainResGetUser(
        user_id=user.id,
        auth_id=user.auth_id,
        email=user.email,
        user_name=user.user_name,
        is_active=user.is_active,
        github=user.github_id,
        instagram=user.instagram_id
    )
    return response

async def service_update_user(user_id:int, db: Session, request_data: DomainReqPutUser):
    user = get_item(User, user_id, db)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Requested user not found")

    user.user_name = request_data.user_name or user.user_name
    user.github_id = request_data.github or user.github_id
    user.instagram_id = request_data.instagram or user.instagram_id

    db.commit()
    db.refresh(user)

    response = DomainResPutUser(
        user_id=user.id,
        auth_id=user.auth_id,
        email=user.email,
        user_name=user.user_name,
        is_active=user.is_active,
        github=user.github_id,
        instagram=user.instagram_id
    )
    return response
