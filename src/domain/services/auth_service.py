from datetime import timedelta

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from domain.schemas.auth_schemas import RegisterRequest, LoginRequest
from config import Settings
from domain.services.token_service import create_user_tokens
from externals.firebase import sign_in_with_email_and_password
from repositories.models import User


async def register(request: RegisterRequest, db: Session):

    # Check if user information exists in the DB
    user = db.query(User).filter(User.user_name == request.user_name).first()

    # If user information does not exist in the DB, create a new user
    if user is None:
        user = User(
            auth_id=request.user_name,
            auth_type='EXP',
            email="none",
            user_name=request.user_name,
            is_active=True
        )
        db.add(user)
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

# firebase를 사용한 로그인


async def login_with_firebase(request, db: Session):
    # Authenticate user
    # Check if user exists in Firebase

    firebase_response = await sign_in_with_email_and_password(request.email, request.password)
    local_id = firebase_response["localId"]

    # Check if user information exists in the DB
    user = db.query(User).filter(User.auth_id == request.auth_id).first()

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


async def login_with_username(
        request: LoginRequest,
        db: Session):
    # Authenticate user
    # Check if user information exists in the DB
    user = db.query(User).filter(User.auth_id == request.auth_id).first()

    # If user information does not exist in the DB, return error
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # Check if the user is active
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User disabled")

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
