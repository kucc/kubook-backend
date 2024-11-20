from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from dependencies import get_current_active_user, get_db
from domain.services.loan_service import service_read_loans_by_user_id
from domain.services.user_service import service_read_user, service_update_user
from routes.response.loan_response import RouteResGetLoanList
from routes.response.user_response import RouteResGetUser, RouteResPutUser
from routes.request.user_request import RouteReqPutUser

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(get_current_active_user)]
)


@router.get(
    "/{user_id}/loans",
    response_model=RouteResGetLoanList,
    status_code=status.HTTP_200_OK,
    summary="회원의 전체 대출 목록 조회",
)
async def get_all_user_loans(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user)
):
    result = await service_read_loans_by_user_id(current_user.id, db)

    response = RouteResGetLoanList(
        data=result,
        count=len(result)
    )
    return response

@router.get(
    "/my-info",
    response_model=RouteResGetUser,
    status_code=status.HTTP_200_OK,
    summary="내 회원정보 조회"
)
async def get_user(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user)
):
    result = await service_read_user(current_user.id, db)

    response = RouteResGetUser(
        user_id=result.user_id,
        auth_id=result.auth_id,
        email=result.email,
        user_name=result.email,
        is_active=result.is_active,
        github=result.github,
        instagram=result.instagram
    )
    return response

@router.put(
    "/my-info",
    response_model=RouteResPutUser,
    status_code=status.HTTP_200_OK,
    summary="내 회원정보 수정"
)
async def put_user(
    request_data: RouteReqPutUser,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user)
):
    result = await service_update_user(current_user.id, db, request_data)

    response = RouteResPutUser(
        user_id=result.user_id,
        auth_id=result.auth_id,
        email=result.email,
        user_name=result.email,
        is_active=result.is_active,
        github=result.github,
        instagram=result.instagram
    )
    return response

