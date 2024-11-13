from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from dependencies import get_current_admin, get_db
from domain.schemas.book_schemas import DomainReqAdminPostBook
from domain.services.admin.book_service import service_admin_create_book
from routes.admin.request.book_request import RouteReqAdminPostBook
from routes.admin.response.book_response import RouteResAdminPostBook

router = APIRouter(
    prefix="/admin/books",
    tags=["admin/books"],
    dependencies=[Depends(get_current_admin)]
)


@router.post(
    "/",
    summary="관리자 도서 정보 등록",
    status_code=status.HTTP_201_CREATED
)
async def create_admin_book(
    request: RouteReqAdminPostBook,
    db: Session = Depends(get_db),
):
    domain_req = DomainReqAdminPostBook(
      book_title = request.book_title,
      code=request.code,
      category_name = request.category_name,
      subtitle=request.subtitle if request.subtitle is not None else None,
      author=request.author,
      publisher=request.publisher,
      publication_year=request.publication_year,
      image_url = request.image_url if request.image_url is not None else None,
      version = request.version if request.version is not None else None,
      major = request.major,
      language=request.language,
      donor_name = request.donor_name if request.donor_name is not None else None
    )
    domain_res = await service_admin_create_book(domain_req, db)
    result = RouteResAdminPostBook(
        book_id=domain_res.id,
        book_title=domain_res.book_title,
        code=domain_res.code,
        category_name=domain_res.category_name,
        subtitle=domain_res.subtitle,
        author=domain_res.author,
        publisher=domain_res.publisher,
        publication_year=domain_res.publication_year,
        image_url=domain_res.image_url,
        version=domain_res.version,
        major=domain_res.major,
        language=domain_res.language,
        book_status=domain_res.book_status,
        donor_name=domain_res.donor_name,
        created_at=domain_res.created_at,
        updated_at=domain_res.updated_at
    )
    return result
