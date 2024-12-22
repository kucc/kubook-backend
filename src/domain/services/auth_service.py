from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from config import Settings
from domain.schemas.auth_schemas import LoginRequest, RegisterRequest
from domain.services.token_service import create_user_tokens, refresh_user_tokens
from externals.firebase import sign_in_with_email_and_password
from repositories.models import User


async def register(request: RegisterRequest, db: Session):

    # Check if user information exists in the DB
    user = db.query(User).filter((User.user_name == request.user_name) | (User.email == request.email)).first()

    # If user information does not exist in the DB, create a new user
    if user is None:
        user = User(
            auth_id=request.user_name,
            auth_type='EXP',
            email=request.email,
            github_id=request.github,
            instagram_id=request.instagram,
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
    response = JSONResponse(content={
        "id": user.id,
        "user_name": user.user_name,
        "is_active": user.is_active,
        "email": user.email
    }, status_code=status.HTTP_201_CREATED)
    response.headers["Authorization"] = token_response["access_token"]
    response.set_cookie(key="refresh_token", value=token_response["refresh_token"],
                        httponly = True, secure=False, samesite="Lax")
    return response

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

    # Create JWT tokens
    token_response = create_user_tokens(user.id)
    response = JSONResponse(content={
        "id": user.id,
        "user_name": user.user_name,
        "is_active": user.is_active,
        "email": user.email
    }, status_code=status.HTTP_200_OK)
    response.headers["Authorization"] = token_response["access_token"]
    response.set_cookie(key="refresh_token", value=token_response["refresh_token"])
    return response

async def service_refresh_token(access_token: str, refresh_token: str):
    token_response = refresh_user_tokens(access_token, refresh_token)
    response = JSONResponse(content=None, status_code=status.HTTP_202_ACCEPTED)
    response.headers["Authorization"]= token_response["access_token"]
    response.set_cookie(key="refresh_token", value=token_response["refresh_token"])
    return response
