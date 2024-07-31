from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from src.core.dependencies import get_db, get_current_admin
from src.domains.services.admin_service import *
import src.domains.model.admin_schemas as s
import src.repositories.models as m

router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)

"""
- POST /admin/books: 도서 정보 등록 (관리자 권한 필요)
- PUT /admin/books/{book_id}: 도서 정보 수정 (관리자 권한 필요)
- DELETE /admin/books/{book_id}: 도서 정보 삭제 (관리자 권한 필요)
- POST /admin/notifications: 알림 생성 (관리자 권한 필요)
- GET /admin/book-requests: 도서 구매 요청 목록 조회 (관리자 권한 필요)
- GET /admin/book-requests/{request_id}: 도서 구매 요청 상세 정보 조회 (관리자 권한 필요)
- PUT /admin/book-requests/{request_id}: 도서 구매 요청 수정 (관리자 권한 필요)
- DELETE /admin/book-requests/{request_id}: 도서 구매 요청 삭제 (관리자 권한 필요)
- GET /admin/users: 전체 사용자 목록 조회 (관리자 권한 필요)
- PUT /admin/users/{user_id}: 사용자 정보 수정 (관리자 권한 필요)
- DELETE /admin/users/{user_id}: 사용자 정보 삭제 (관리자 권한 필요)
- GET /admin/loans: 전체 대출 목록 조회 (관리자 권한 필요)
- GET /admin/reservations: 전체 예약 목록 조회 (관리자 권한 필요)
- POST /admin/notices: 공지사항 등록 (관리자 권한 필요)
- PUT /admin/notices/{notice_id}: 공지사항 수정 (관리자 권한 필요)
- DELETE /admin/notices/{notice_id}: 공지사항 삭제 (관리자 권한 필요)
- GET /admin/settings: 시스템 설정 조회 (관리자 권한 필요)
- PUT /admin/settings: 시스템 설정 수정 (관리자 권한 필요)
"""


@router.delete(
    "/dba",
    summary="data 완전 삭제",
    status_code=status.HTTP_200_OK
)
async def delete_data(index: int, db: Session = Depends(get_db), current_user=Depends(get_current_admin)):
    return delete_item_dba(m.BookInfo, index, current_user, db)

# =================== 도서 정보 =========================


@router.get(
    "/book-info",
    summary="도서 정보 목록 조회",
    response_model=List[s.BookInfo],
    status_code=status.HTTP_200_OK
)
async def get_list_book_info(db: Session = Depends(get_db), current_user=Depends(get_current_admin)):
    return get_list(m.BookInfo, current_user, db)


@router.get(
    "/book-info/{book_info_id}",
    summary="도서 정보 조회",
    response_model=s.BookInfo,
    status_code=status.HTTP_200_OK
)
async def get_book_info(book_info_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_admin)):
    return get_item(m.BookInfo, book_info_id, current_user, db)


@router.post(
    "/book-info",
    summary="도서 정보 등록",
    response_model=s.BookInfo,
    status_code=status.HTTP_201_CREATED
)
async def create_book_info(book_info_data: s.BookInfoCreate, db: Session = Depends(get_db), current_user=Depends(get_current_admin)):
    return create_item(m.BookInfo, book_info_data, current_user, db)


@router.patch(
    "/book-info/{book_info_id}",
    summary="도서 정보 수정",
    response_model=s.BookInfo,
    status_code=status.HTTP_200_OK
)
async def update_book_info(book_info_id: int, book_info_data: s.BookInfoUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_admin)):
    return update_item(m.BookInfo, book_info_data, book_info_id, current_user, db)


@router.delete(
    "/book-info/{book_info_id}",
    summary="도서 정보 삭제",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_book_info(book_info_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_admin)):
    return delete_item(m.BookInfo, book_info_id, current_user, db)

# =================== 책 정보 =========================


@router.get(
    "/books",
    summary="책 정보 목록 조회",
    response_model=List[s.Book],
    status_code=status.HTTP_200_OK
)
async def get_list_books(db: Session = Depends(get_db), current_user=Depends(get_current_admin)):
    return get_list(m.Book, current_user, db)


@router.get(
    "/books/{book_id}",
    summary="책 정보 조회",
    response_model=s.Book,
    status_code=status.HTTP_200_OK
)
async def get_book_info(book_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_admin)):
    return get_item(m.Book, book_id, current_user, db)


@router.post(
    "/books",
    summary="책 정보 등록",
    response_model=s.Book,
    status_code=status.HTTP_201_CREATED
)
async def create_book(book_data: BookCreate, db: Session = Depends(get_db), current_user=Depends(get_current_admin)):
    return create_item(m.Book, book_data, current_user, db)


@router.patch(
    "/books/{book_id}",
    summary="책 정보 수정",
    response_model=s.Book,
    status_code=status.HTTP_200_OK
)
async def update_book(book_id: int, book_data: BookUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_admin)):
    return update_item(m.Book, book_data, book_id, current_user, db)


@router.delete(
    "/books/{book_id}",
    summary="책 정보 삭제",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_book(book_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_admin)):
    return delete_item(m.Book, book_id, current_user, db)
# =================== 카테고리 =========================


@router.get(
    "/category",
    summary="전체 카테고리 목록 조회",
    response_model=List[s.Category],
    status_code=status.HTTP_200_OK
)
async def get_list_category(db: Session = Depends(get_db), current_user=Depends(get_current_admin)):
    return get_list(m.BookCategory, current_user, db)


@router.get(
    "/category/{category_id}",
    summary="카테고리 정보 조회",
    response_model=s.Category,
    status_code=status.HTTP_200_OK
)
async def get_category(category_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_admin)):
    return get_item(m.BookCategory, category_id, current_user, db)


@router.post(
    "/category",
    summary="카테고리 생성",
    response_model=s.Category,
    status_code=status.HTTP_201_CREATED
)
async def create_category(category_data: CategoryCreate, db: Session = Depends(get_db), current_user=Depends(get_current_admin)):
    return create_item(m.BookCategory, category_data, current_user, db)


@router.patch(
    "/category/{category_id}",
    summary="카테고리 정보 수정",
    response_model=s.Category,
    status_code=status.HTTP_200_OK
)
async def update_category(category_id: int, category_data: CategoryUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_admin)):
    return update_item(m.BookCategory, category_data, category_id, current_user, db)


@router.delete(
    "/category/{category_id}",
    summary="카테고리 정보 삭제",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_category(category_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_admin)):
    return delete_item(m.BookCategory, category_id, current_user, db)

# =================== 도서 구매 요청 =========================


@router.get(
    "/book-requests",
    summary="도서 구매 요청 목록 조회",
    response_model=List[s.BookRequest],
    status_code=status.HTTP_200_OK
)
async def get_list_book_requests(db: Session = Depends(get_db), current_user=Depends(get_current_admin)):
    return get_list(m.RequestedBook, current_user, db)


@router.get(
    "/book-requests/{request_id}",
    summary="도서 구매 요청 정보 조회",
    response_model=s.BookRequest,
    status_code=status.HTTP_200_OK
)
async def get_book_request(request_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_admin)):
    return get_item(m.RequestedBook, request_id, current_user, db)


@router.patch(
    "/book-requests/{request_id}",
    summary="도서 구매 요청 수정",
    response_model=s.BookRequest,
    status_code=status.HTTP_200_OK
)
async def update_book_request(request_id: int, request_data: BookRequestUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_admin)):
    return update_item(m.RequestedBook, request_data, request_id, current_user, db)


@router.delete(
    "/book-requests/{request_id}",
    summary="도서 구매 요청 삭제(미개발)",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_book_request(request_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_admin)):
    return delete_item(m.RequestedBook, request_id, current_user, db)

# =================== 사용자 정보 =========================


@router.get(
    "/users",
    summary="전체 사용자 목록 조회",
    response_model=List[s.User],
    status_code=status.HTTP_200_OK
)
async def get_list_user(db: Session = Depends(get_db), current_user=Depends(get_current_admin)):
    pass


@router.get(
    "/users/{user_id}",
    summary="사용자 정보 조회",
    response_model=s.User,
    status_code=status.HTTP_200_OK
)
async def get_user(user_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_admin)):
    pass


@router.patch(
    "/users/{user_id}",
    summary="사용자 정보 수정",
    response_model=s.User,
    status_code=status.HTTP_200_OK
)
async def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_admin)):
    pass


@router.delete(
    "/users/{user_id}",
    summary="사용자 정보 삭제",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_user(user_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_admin)):
    pass

# =================== 대출 정보 =========================


@router.get(
    "/loans",
    summary="전체 대출 목록 조회",
    response_model=List[s.Loan],
    status_code=status.HTTP_200_OK
)
async def get_list_loans(db: Session = Depends(get_db), current_user=Depends(get_current_admin)):
    pass


@router.get(
    "/loans/{loan_id}",
    summary="대출 정보 조회",
    response_model=s.Loan,
    status_code=status.HTTP_200_OK
)
async def get_loan(loan_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_admin)):
    pass


@router.patch(
    "/loans/{loan_id}",
    summary="대출 정보 수정",
    response_model=s.Loan,
    status_code=status.HTTP_200_OK
)
async def update_loan(loan_id: int, loan: LoanUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_admin)):
    pass


@router.delete(
    "/loans/{loan_id}",
    summary="대출 정보 삭제",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_loan(loan_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_admin)):
    pass

# =================== 예약 정보 =========================


@router.get(
    "/reservations",
    summary="전체 예약 목록 조회",
    response_model=List[s.Reservation],
    status_code=status.HTTP_200_OK
)
async def get_list_reservations(db: Session = Depends(get_db), current_user=Depends(get_current_admin)):
    pass


@router.get(
    "/reservations/{reservation_id}",
    summary="예약 정보 조회",
    response_model=s.Reservation,
    status_code=status.HTTP_200_OK
)
async def get_reservation(reservation_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_admin)):
    pass


@router.patch(
    "/reservations/{reservation_id}",
    summary="예약 정보 수정",
    response_model=s.Reservation,
    status_code=status.HTTP_200_OK
)
async def update_reservation(reservation_id: int, reservation: ReservationUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_admin)):
    pass


@router.delete(
    "/reservations/{reservation_id}",
    summary="예약 정보 삭제",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_reservation(reservation_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_admin)):
    pass

# =================== 공지사항 =========================


@router.get(
    "/notices",
    summary="전체 공지사항 목록 조회",
    response_model=List[s.Notice],
    status_code=status.HTTP_200_OK
)
async def get_list_notices(db: Session = Depends(get_db), current_user=Depends(get_current_admin)):
    pass


@router.get(
    "/notices/{notice_id}",
    summary="공지사항 조회",
    response_model=s.Notice,
    status_code=status.HTTP_200_OK
)
async def get_notice(notice_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_admin)):
    pass


@router.post(
    "/notices",
    summary="공지사항 등록",
    response_model=s.Notice,
    status_code=status.HTTP_201_CREATED
)
async def create_notice(notice: NoticeCreate, db: Session = Depends(get_db), current_user=Depends(get_current_admin)):
    pass


@router.patch(
    "/notices/{notice_id}",
    summary="공지사항 수정",
    response_model=s.Notice,
    status_code=status.HTTP_200_OK
)
async def update_notice(notice_id: int, notice: NoticeUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_admin)):
    pass


@router.delete(
    "/notices/{notice_id}",
    summary="공지사항 삭제",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_notice(notice_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_admin)):
    pass

# =================== 시스템 설정 =========================


@router.get(
    "/settings",
    summary="전체 시스템 설정 목록 조회",
    response_model=List[s.ServiceSetting],
    status_code=status.HTTP_200_OK
)
async def list_get_settings(db: Session = Depends(get_db), current_user=Depends(get_current_admin)):
    pass


@router.get(
    "/settings/{setting_id}",
    summary="시스템 설정 조회",
    response_model=s.ServiceSetting,
    status_code=status.HTTP_200_OK
)
async def get_settings(setting_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_admin)):
    pass


@router.post(
    "/settings",
    summary="시스템 설정 등록",
    response_model=s.ServiceSetting,
    status_code=status.HTTP_201_CREATED
)
async def create_settings(settings: ServiceSettingCreate, db: Session = Depends(get_db), current_user=Depends(get_current_admin)):
    pass


@router.patch(
    "/settings/{setting_id}",
    summary="시스템 설정 수정",
    response_model=s.ServiceSetting,
    status_code=status.HTTP_200_OK
)
async def update_settings(setting_id: int, settings: ServiceSettingUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_admin)):
    pass


@router.delete(
    "/settings/{setting_id}",
    summary="시스템 설정 삭제",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_settings(setting_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_admin)):
    pass
