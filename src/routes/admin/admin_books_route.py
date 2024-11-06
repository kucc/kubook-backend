from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from dependencies import get_current_admin, get_db
from domain.schemas.book_schemas import DomainReqAdminPostBook
from domain.services.admin.book_service import service_admin_create_book
from routes.admin.request.book_request import RouteReqAdminPostBook

router = APIRouter(
    prefix="/admin/books",
    tags=["admin/books"],
    dependencies=[Depends(get_current_admin)]
)


@router.post(
    "/",
    summary="관리자 도서 정보 등록",
    status_code=status.HTTP_200_OK
)
async def create_admin_book(
    request: RouteReqAdminPostBook,
    db: Session = Depends(get_db),
):
    domain_req = DomainReqAdminPostBook(
      book_title = request.book_title,
      code=request.code,
      category_name = request.category_name,
      subtitle=request.subtitle,
      author=request.autor,
      publisher=request.publisher,
      publication_year=request.publication_year,
      image_url = request.image_url,
      version = request.version,
      major = request.major,
      donor_name = request.donor_name
    )
    await service_admin_create_book(domain_req, db)
    return
