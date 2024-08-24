from datetime import date
from datetime import datetime as _datetime
from datetime import timedelta
from typing import List, Optional

from pydantic import BaseModel, Field


class ItemBase(BaseModel):
    created_at: _datetime = Field(..., title="create_at", description="생성일시", example=_datetime.now())
    updated_at: _datetime = Field(..., title="update_at", description="수정일시", example=_datetime.now())
    is_valid: bool = Field(..., title="is_valid", description="유효 여부", example=True)

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.__annotations__['id'] = int
        cls.id = Field(..., title="id", description=f'{cls.__name__.lower()} id', example=1, ge=0)

# ===============================================================


class CategoryBase(BaseModel):
    code: str = Field(..., title="code", description="카테고리 코드", example="A")
    name: str = Field(..., title="name", description="카테고리명", example="인공지능")


class Category(CategoryBase, ItemBase):
    pass


class CategoryCreate(CategoryBase):
    pass


# class CategoryUpdate(CategoryBase.all_optional("CategoryUpdate")):
#     pass

# =======================================================================


class BookInfoBase(BaseModel):
    title: str = Field(..., title="title", description="책 제목", example="FastAPI Tutorial")
    subtitle: Optional[str] = Field(None, title="subtitle", description="책 부제목", example="Build modern web APIs with Python and FastAPI")
    author: str = Field(..., title="author", description="저자", example="John Doe")
    publisher: str = Field(..., title="publisher", description="출판사", example="AA Publisher")
    publication_year: int = Field(..., title="publication_year", description="출판년도", example=_datetime.now().year)
    image_url: Optional[str] = Field(None, title="image_url", description="이미지 URL", example="https://example.com/image.jpg")
    category_id: int = Field(..., title="category_id", description="카테고리 ID", example=1, ge=0)
    version: Optional[str] = Field(None, title="version", description="책 버전", example="1판")
    major: Optional[bool] = Field(False, title="major", description="전공 도서 여부", example=False)
    language: Optional[bool] = Field(True, title="language", description="True: 국문, False: 영문", example=True)


class BookInfo(BookInfoBase, ItemBase):
    pass


class BookInfoCreate(BookInfoBase):
    pass


# class BookInfoUpdate(BookInfoBase.all_optional("BookInfoUpdate")):
#     pass

# ===============================================================


class BookBase(BaseModel):
    book_info_id: int = Field(..., title="book_info_id", description="책과 연결된 도서 정보 id", example=1, ge=0)
    book_status: int = Field(0, title="book_status", description="책 상태", example=1, ge=0, le=3)
    note: Optional[str] = Field(None, title="note", description="노트", example="기부된 책")
    donor_name: Optional[str] = Field(None, title="donor_name", description="기부자 이름", example="김철수")


class Book(BookBase, ItemBase):
    pass


# class BookCreate(BookBase.omit_fields('BookCreate', ['book_status'])):
#     pass


# class BookUpdate(BookBase.all_optional("BookUpdate")):
#     pass
# ==================================================================


class UserBase(BaseModel):
    user_name: str = Field(..., title="user_name", description="사용자 이름", example="JohnDoe")
    is_active: bool = Field(True, title="is_active", description="활성 상태", example=True)
    email: str = Field(..., title="email", description="이메일", example="john.doe@example.com")


class User(UserBase, ItemBase):
    pass


# class UserUpdate(UserBase.all_optional("UserUpdate")):
#     pass

# ===============================================================


class BookRequestBase(BaseModel):
    user_id: int = Field(..., title="user_id", description="도서 구매를 요청한 사용자 ID", example=1, ge=0)
    book_title: str = Field(..., title="book_title", description="책 제목", example="FastAPI Tutorial")
    publication_year: Optional[int] = Field(..., title="publication_year", description="출판년도", example=2022, ge=0)
    request_link: str = Field(..., title="request_link", description="요청 링크", example="https://example.com/request")
    reason: str = Field(..., title="reason", description="이유", example="Need for study")


class BookRequestInfo(BookRequestBase):
    processing_status: int = Field(0, title="processing_status", description="처리 상태", example=0, ge=0, le=3)
    request_date: date = Field(..., title="request_date", description="요청 일자", example=_datetime.now().date())
    reject_reason: Optional[str] = Field(None, title="reject_reason", description="거절 사유", example="Not available")


class BookRequest(BookRequestInfo, ItemBase):
    pass


class BookRequestCreate(BookRequestBase):
    pass


# class BookRequestUpdate(BookRequestInfo.all_optional("BookRequestUpdate")):
#     pass


# ===============================================================

class LoanBase(BaseModel):
    book_id: int = Field(..., title="book_id", description="대출한 책 ID", example=1, ge=0)
    user_id: int = Field(..., title="user_id", description="대출한 사용자 ID", example=1, ge=0)


class LoanInfo(LoanBase):
    loan_date: date = Field(..., title="loan_date", description="대출 날짜", example=_datetime.today().date())
    due_date: date = Field(..., title="due_date", description="반납 기한", example=(_datetime.today() + timedelta(days=14)).date())
    extend_status: bool = Field(False, title="extend_status", description="연장 상태", example=True)
    overdue_days: int = Field(0, title="overdue_days", description="연체 일자", example=1, )
    return_status: bool = Field(False, title="return_status", description="반납 상태", example=False, )
    return_date: Optional[date] = Field(None, title="return_date", description="반납 날짜", example=None)


class Loan(LoanInfo, ItemBase):
    pass


class LoanCreate(LoanBase):
    pass


# class LoanUpdate(LoanInfo.all_optional("LoanUpdate")):
#     pass


# =======================================================================

class ReservationBase(BaseModel):
    book_id: int = Field(..., title="book_id", description="예약한 책 ID", example=1, ge=0)
    user_id: int = Field(..., title="user_id", description="예약한 사용자 ID", example=1, ge=0)
    reservation_date: date = Field(..., title="reservation_date", description="예약 날짜", example=_datetime.now().date())
    reservation_status: int = Field(0, title="reservation_status", description="예약 상태", example=0, ge=0, le=3)


class Reservation(ReservationBase, ItemBase):
    pass


# class ReservationCreate(ReservationBase.omit_fields("ReservationCreate", ["reservation_date", "reservation_status"])):
#     pass


# class ReservationUpdate(ReservationBase.all_optional("ReservationUpdate")):
#     pass


# =======================================================================

class AdminBase(BaseModel):
    user_id: int = Field(..., title="user_id", description="관리자의 일반 ID", example=1, ge=0)
    admin_status: bool = Field(..., title="reservation_status", description="관리자 상태", example=True)
    expiration_date: date = Field(..., title="expiration_date", description="권한 기한", example=(_datetime.now() + timedelta(days=365)).date())


class Admin(AdminBase, ItemBase):
    pass


class AdminCreate(AdminBase):
    pass


# class AdminUpdate(AdminBase.all_optional("AdminUpdate")):
#     pass

# ==============================================================


class NoticeBase(BaseModel):
    admin_id: int = Field(..., title="admin_id", description="작성자(관리자)의 관리자 ID", example=1, ge=0)
    title: str = Field(..., title="title", description="공지 제목", example="Scheduled Maintenance")
    notice_content: Optional[str] = Field(None, title="notice_content", description="공지 내용", example="The system will be down for maintenance.")


class Notice(NoticeBase, ItemBase):
    pass


class NoticeCreate(NoticeBase):
    pass


# class NoticeUpdate(NoticeBase.all_optional("NoticeUpdate")):
#     pass


# ==================================================================

class ServiceSettingBase(BaseModel):
    name: str = Field(..., title="name", description="설정 이름", example="service_begin")
    data_type: str = Field(..., title="datatype", description="데이터 유형", example="datetime")
    value: str = Field(..., title="value", description="설정 값", example=_datetime.today())
    description: Optional[str] = Field(None, title="description", description="설정 설명", example="서비스가 시작하는 날짜. 해당 일시 이후로 대출, 반납, 예약, 도서 구매요청 가능")


class ServiceSetting(ServiceSettingBase, ItemBase):
    pass


class ServiceSettingCreate(ServiceSettingBase):
    pass


# class ServiceSettingUpdate(ServiceSetting.all_optional("ServiceSettingUpdate")):
#     pass


# =============================== 전체 조회 Response 클래스 ====================

class BookInfoRes(BookInfo):
    books: List[Book]


class BookRes(Book):
    book_info: BookInfo


class CategoryRes(Category):
    books: List[BookInfo]


class BookRequestRes(BookRequest):
    user: UserBase


class LoanRes(Loan):
    book: BookRes
    user: UserBase


class ReservationRes(Reservation):
    book: BookRes
    user: UserBase


class AdminRes(Admin):
    user: UserBase


class UserRes(User):
    requested_books: List[BookRequest]
    reservations: List[Reservation]
    loans: List[Loan]
    admin: Optional[Admin]


class NoticeRes(Notice):
    admin: AdminRes
