from datetime import timedelta


from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from src.core.config import Settings
from src.repositories.models import User
from src.externals.firebase import sign_in_with_email_and_password
from src.domains.services.token_service import create_user_tokens


async def register(current_user, request, db: Session):

    user_id = current_user.id

    # Check if user information exists in the DB
    user = db.query(User).filter(User.id == user_id).first()

    # If user name is TEMP_USER_NAME(not registered), update user name, else reutrn error(already registered)
    if user.user_name == Settings().TEMP_USER_NAME:
        user.user_name = request.user_name
        user.is_active = request.is_active
        db.commit()
        db.refresh(user)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

    # Create JWT tokens
    token_response = create_user_tokens(user.id)

    return {
        "token": token_response,
        "user": {
            "id": user.id,
            "user_name": user.user_name,
            "is_active": user.is_active,
            "email": user.email
        }
    }


async def login(request, db: Session):
    # Authenticate user
    # Check if user exists in Firebase

    firebase_response = await sign_in_with_email_and_password(request.email, request.password)
    local_id = firebase_response["localId"]

    # Check if user information exists in the DB
    user = db.query(User).filter(User.auth_id == local_id).first()

    # If user information does not exist in the DB, create a new user
    user_info_required = False
    if user is None:
        user = User(
            auth_id=local_id,
            user_name=Settings().TEMP_USER_NAME,
            email=request.email
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        user_info_required = True

    # Create JWT tokens
    token_response = create_user_tokens(user.id)

    if user_info_required:
        return {
            "token": token_response,
            "user_info_required": True
        }
    else:
        return {
            "token": token_response,
            "user": {
                "id": user.id,
                "user_name": user.user_name,
                "is_active": user.is_active,
                "email": user.email
            }
        }
