from typing import Annotated

from fastapi import APIRouter, Cookie, Depends, Header, status
from sqlalchemy.orm import Session

import domain.schemas.auth_schemas as auth_schemas
from config import Settings
from dependencies import get_db
from domain.services.auth_service import service_login, service_refresh_token, service_register

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

settings = Settings()

# 신규 사용자 등록


@router.post(
    "/register",
    response_model=auth_schemas.RegisterResponse,
    status_code=status.HTTP_201_CREATED,
    summary="신규 사용자 등록",
    description="""신규 사용자 등록
    """,
    response_description={
        status.HTTP_201_CREATED: {"description": "User created"},
        status.HTTP_400_BAD_REQUEST: {"description": "User already exists"}
    }
)
async def register(
    request: auth_schemas.RegisterRequest,
    db: Session = Depends(get_db)
):
    return await service_register(request, db)


@router.post(
    "/login",
    response_model=auth_schemas.LoginResponse,
    status_code=status.HTTP_200_OK,
    summary="로그인",
    description="""
    - 사용자가 이메일과 비밀번호를 입력한 후 로그인 버튼을 클릭
    - Firebase에 사용자 정보가 존재하지 않으면 (프론트에서) LMS에서 회원가입하라고 안내
    - Firebase에 사용자 정보가 존재할 경우 쿠책책의 DB에 사용자 정보가 있는지 확인
    - 만약 사용자 정보가 있다면 로그인 처리
    - 사용자 정보가 없다면 회원가입 페이지로 이동
        - 그런데 회원가입 페이지에서 추가로 입력할 내용이 거의 없어서 회원가입 API POST /auth/register는 Deprecated 처리
        - 추후 회원가입 시 기입할 정보가 늘어난다면 POST /auth/register를 다시 활성화할 것
    """,
    response_description={
        status.HTTP_200_OK: {"description": "Login successful"},
        status.HTTP_404_NOT_FOUND: {"description": "User not found"},
        status.HTTP_401_UNAUTHORIZED: {"description": "Invalid password"},
        status.HTTP_403_FORBIDDEN: {"description": "User disabled"},
    }
)
async def login(
    request: auth_schemas.LoginRequest,
    db: Session = Depends(get_db)
):
    if settings.ENVIRONMENT == "development":
        return await service_login(request, db)
    # elif settings.ENVIRONMENT == "production":
    #     return await auth_service.login(request, db)

@router.post(
    "/refresh-token",
    status_code=status.HTTP_201_CREATED,
    summary="토큰 재발급",
    description="refresh_token(Cookie)이 유효한 경우에만 토큰 재발급 가능",
    response_description={
        status.HTTP_201_CREATED: {"description": "Created New Tokens"},
        status.HTTP_208_ALREADY_REPORTED: {"description": "Available Tokens"},
        status.HTTP_410_GONE: {"description": "Invalid / Expired Refresh Token"},
    }
)
async def refresh_token(
    access_token: str = Header(),
    refresh_token: Annotated[str, Cookie()] = None
):
    return await service_refresh_token(access_token = access_token, refresh_token = refresh_token)
