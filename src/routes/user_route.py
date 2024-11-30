from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from dependencies import get_current_user, get_db
from domain.schemas.bookrequest_schemas import DomainReqGetBookRequest
from domain.services.bookrequest_service import service_read_bookrequest_list
from domain.services.loan_service import service_read_loans_by_user_id
from domain.services.user_service import service_read_user, service_update_user
from routes.request.user_request import RouteReqPutUser
from routes.response.bookrequest_response import RouteResBookRequest, RouteResBookRequestList
from routes.response.loan_response import RouteResGetLoanList
from routes.response.user_response import RouteResGetUser, RouteResPutUser

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(get_current_user)]
)

@router.get(
    "/my-loans",
    response_model=RouteResGetLoanList,
    status_code=status.HTTP_200_OK,
    summary="회원의 전체 대출 목록 조회",
)
async def get_all_user_loans(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
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
    current_user=Depends(get_current_user)
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

@router.get(
    "/my-requests",
    summary="user의 도서 구매 요청 목록 조회",
    response_model=RouteResBookRequestList,
    status_code=status.HTTP_200_OK,
)
async def get_user_bookrequests(
    db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    domain_req = DomainReqGetBookRequest(user_id=current_user.id)
    domain_res = await service_read_bookrequest_list(domain_req, db)
    converted_res = [
        RouteResBookRequest(
            user_id=item.user_id,
            request_id=item.request_id,
            book_title=item.book_title,
            publication_year=item.publication_year,
            request_link=item.request_link,
            reason=item.reason,
            processing_status=item.processing_status,
            request_date=item.request_date,
            reject_reason=item.reject_reason,
        )
        for item in domain_res
    ]

    result = RouteResBookRequestList(data=converted_res, count=len(converted_res))
    return result

@router.put(
    "/my-info",
    response_model=RouteResPutUser,
    status_code=status.HTTP_200_OK,
    summary="내 회원정보 수정"
)
async def put_user(
    request: RouteReqPutUser,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    result = await service_update_user(current_user.id, db, request)

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

