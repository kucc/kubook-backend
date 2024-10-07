from pydantic import BaseModel, Field
from typing import Optional

class RouteReqPutUser(BaseModel):
    user_name: str = Field(title="user_name", description="사용자 이름", example="홍길동")
    github: str | None = Field(None, title="github", description="깃허브 주소", example="https://github.com/kucc")
    instagram: str | None = Field(None, title="instagram", description="인스타그램 주소", example="https://www.instagram.com/")