from typing import Optional
from pydantic import BaseModel, Field


class UserInfo(BaseModel):
    id: int
    user_name: str
    is_active: bool
    email: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class FirebaseLoginRequest(BaseModel):
    email: str = Field(..., example="test@test.com")
    password: str = Field(..., example="asdf1234")


class LoginRequest(BaseModel):
    email: str = Field(..., example="test@test.com")
    password: str = Field(..., example="asdf1234")


class LoginResponse(BaseModel):
    token: TokenResponse = None
    user: UserInfo = None
    user_info_required: bool = False


class RegisterRequest(BaseModel):
    email: str = Field(..., example="test@test.com")
    password: str = Field(..., example="asdf1234")
    user_name: str = Field(..., example="테스트 이름")
    github: Optional[str] = Field(default=None)
    instagram: Optional[str] = Field(default=None)
    is_active: bool = Field(..., example=True)


class RegisterResponse(BaseModel):
    token: TokenResponse = None
    user: UserInfo = None
