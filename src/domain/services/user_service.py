from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from domain.schemas.user_schemas import DomainReqPutUser, DomainResGetUser, DomainResPutUser
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

async def service_update_user(user_id:int, db: Session, request: DomainReqPutUser):
    user = get_item(User, user_id, db)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Requested user not found")

    if request.user_name :
        user.user_name = request.user_name
    if request.github :
        user.github_id = request.github
    if request.instagram :
        user.instagram_id = request.instagram

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
