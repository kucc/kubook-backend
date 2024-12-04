from fastapi import HTTPException, status
from pydantic import BaseModel, Field, model_validator


class RouteReqPutUser(BaseModel):
    user_name: str | None = Field(title="user_name", description="사용자 이름", example="홍길동")
    github: str | None = Field(None, title="github", description="깃허브 주소", example="https://github.com/kucc")
    instagram: str | None = Field(None,title="instagram", description="인스타그램 주소", example="https://www.instagram.com/")

    @model_validator(mode="before")
    def check_at_least_one_field(cls, values):
        # If all three fields are FALSY VALUE, raise an error
        if not any(values.get(field) for field in ['user_name', 'github', 'instagram']):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="At least 'user_name', 'github', or 'instagram' must be provided."
            )
        return values
