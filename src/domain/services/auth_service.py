from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from config import Settings
from domain.schemas.auth_schemas import LoginRequest, LoginResponse, RegisterRequest, RegisterResponse, UserInfo
from domain.services.token_service import create_user_tokens, refresh_user_tokens, verify_token
from externals.firebase import sign_in_with_email_and_password
from repositories.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
async def register(request: RegisterRequest, db: Session):

    # Check if user information exists in the DB
    user = db.query(User).filter(User.email == request.email).first()

    # If user information does not exist in the DB, create a new user
    if user is None:
        hashed_pwd = pwd_context.hash(request.password)
        user = User(
            auth_id=request.user_name,
            auth_type='EXP',
            email=request.email,
            github_id=request.github,
            instagram_id=request.instagram,
            user_name=request.user_name,
            password=hashed_pwd,
            is_active=True
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

    # Create JWT tokens
    token_response = create_user_tokens(user.id)
    user_info = RegisterResponse(
        user=UserInfo(
            id=user.id,
            user_name=user.user_name,
            email=user.email,
            is_active=user.is_active
        )
    ).model_dump()
    response = JSONResponse(content=user_info, status_code=status.HTTP_201_CREATED)

    response.headers["Authorization"] = token_response["access_token"]
    response.set_cookie(key="refresh_token", value=token_response["refresh_token"],
                        httponly = True, secure=False, samesite="Lax")
    return response

# firebase를 사용한 로그인


async def login_with_firebase(request:LoginRequest, db: Session):
    # Authenticate user
    # Check if user exists in Firebase

    firebase_response = await sign_in_with_email_and_password(request.email, request.password)
    local_id = firebase_response["localId"]

    # Check if user information exists in the DB
    user = db.query(User).filter(User.auth_id == request.auth_id, User.is_deleted==False).first()

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
    login_response = LoginResponse(
        user_info_required,
        user=UserInfo(
            id=user.id,
            user_name=user.user_name,
            email=user.email,
            is_active=user.is_active
        )
    ).model_dump()
    response = JSONResponse(content=login_response, status_code=status.HTTP_200_OK)
    response.headers["Authorization"] = token_response["access_token"]
    response.set_cookie(key="refresh_token", value=token_response["refresh_token"])

    return response


async def login_with_username(
        request: LoginRequest,
        db: Session):
    # Authenticate user
    # Check if user information exists in the DB
    user = db.query(User).filter(User.email == request.email, User.is_deleted==False).first()
    # If user information does not exist in the DB, return error
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if not pwd_context.verify(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Password")

    # Create JWT tokens
    token_response = create_user_tokens(user.id)
    login_response = LoginResponse(
        user_info_required=True,
        user=UserInfo(
            id=user.id,
            user_name=user.user_name,
            email=user.email,
            is_active=user.is_active
        )
    ).model_dump()
    response = JSONResponse(content=login_response, status_code=status.HTTP_200_OK, headers={
        "Authorization" : token_response["access_token"]
    })
    response.headers["Authorization"] = token_response["access_token"]
    response.set_cookie(key="refresh_token", value=token_response["refresh_token"])
    return response

async def service_refresh_token(access_token: str, refresh_token: str):
    try:
        verified_access = verify_token(access_token)
        if verified_access > -1 :
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Available Access Token",
                headers={"WWW-Authenticate": "Bearer"}
            )
        elif verified_access == -1 :
            token_response = refresh_user_tokens(refresh_token)
    except HTTPException as e:
        raise e
    response = JSONResponse(content=None, status_code=status.HTTP_201_CREATED, headers={
        "Authorization" : token_response["access_token"]
    })
    response.set_cookie(key="refresh_token", value=token_response["refresh_token"])
    return response
