from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, DateTime, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    auth_id = Column(String(50), unique=True, nullable=False)
    user_name = Column(String(45), nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    email = Column(String(100), unique=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.current_timestamp())
    updated_at = Column(DateTime, nullable=False, default=func.current_timestamp(), onupdate=func.current_timestamp())
    is_valid = Column(Boolean, nullable=False, default=True)

    requested_books = relationship("RequestedBook", back_populates="user")
    admin = relationship("Admin", uselist=False, back_populates="user")
    book_reviews = relationship("BookReview", back_populates="user")
    reservations = relationship("Reservation", back_populates="user")
    loans = relationship("Loan", back_populates="user")


class RequestedBook(Base):
    __tablename__ = "requested_book"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    book_title = Column(String(255), nullable=False)
    publication_year = Column(Integer)
    reject_reason = Column(Text, nullable=True)
    request_link = Column(String(100), nullable=False)
    reason = Column(Text, nullable=False)
    processing_status = Column(Integer, nullable=False, default=0)
    request_date = Column(Date, nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.current_timestamp())
    updated_at = Column(DateTime, nullable=False, default=func.current_timestamp(), onupdate=func.current_timestamp())
    is_valid = Column(Boolean, nullable=False, default=True)

    user = relationship("User", back_populates="requested_books")


class Admin(Base):
    __tablename__ = "admin"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    admin_status = Column(Boolean, nullable=False)
    expiration_date = Column(Date, nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.current_timestamp())
    updated_at = Column(DateTime, nullable=False, default=func.current_timestamp(), onupdate=func.current_timestamp())
    is_valid = Column(Boolean, nullable=False, default=False)

    user = relationship("User", back_populates="admin")
    notices = relationship("Notice", back_populates="admin")


class Notice(Base):
    __tablename__ = "notice"

    id = Column(Integer, primary_key=True, index=True)
    admin_id = Column(Integer, ForeignKey("admin.id"), nullable=False)
    user_id = Column(Integer)
    title = Column(String(255), nullable=False)
    notice_content = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.current_timestamp())
    updated_at = Column(DateTime, nullable=False, default=func.current_timestamp(), onupdate=func.current_timestamp())
    is_valid = Column(Boolean, nullable=False, default=True)

    admin = relationship("Admin", back_populates="notices")


class BookCategory(Base):
    __tablename__ = "book_category"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(5), nullable=False)
    name = Column(String(50), nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.current_timestamp())
    updated_at = Column(DateTime, nullable=False, default=func.current_timestamp(), onupdate=func.current_timestamp())
    is_valid = Column(Boolean, nullable=False, default=True)

    books = relationship("BookInfo", back_populates="category")


class BookInfo(Base):
    __tablename__ = "book_info"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    subtitle = Column(String(255))
    author = Column(String(100), nullable=False)
    publisher = Column(String(45), nullable=False)
    publication_year = Column(Integer, nullable=False)
    image_url = Column(String(255))
    category_id = Column(Integer, ForeignKey("book_category.id"), nullable=False)
    version = Column(String(45))
    major = Column(Boolean, default=False)
    language = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, default=func.current_timestamp())
    updated_at = Column(DateTime, nullable=False, default=func.current_timestamp(), onupdate=func.current_timestamp())
    is_valid = Column(Boolean, nullable=False, default=True)

    category = relationship("BookCategory", back_populates="books")
    book_stat = relationship("BookStat", back_populates="book_info")
    book_reviews = relationship("BookReview", back_populates="book_info")
    books = relationship("Book", back_populates="book_info")


class BookReview(Base):
    __tablename__ = "book_review"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    book_info_id = Column(Integer, ForeignKey("book_info.id"), nullable=False)
    review_content = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.current_timestamp())
    updated_at = Column(DateTime, nullable=False, default=func.current_timestamp(), onupdate=func.current_timestamp())
    is_valid = Column(Boolean, nullable=False, default=True)

    user = relationship("User", back_populates="book_reviews")
    book_info = relationship("BookInfo", back_populates="book_reviews")


class Book(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True, index=True)
    book_info_id = Column(Integer, ForeignKey("book_info.id"), nullable=False)
    book_status = Column(Integer, nullable=False, default=0)
    note = Column(String(255), default=None)
    donor_name = Column(String(255), default=None)
    created_at = Column(DateTime, nullable=False, default=func.current_timestamp())
    updated_at = Column(DateTime, nullable=False, default=func.current_timestamp(), onupdate=func.current_timestamp())
    is_valid = Column(Boolean, nullable=False, default=False)

    book_info = relationship("BookInfo", back_populates="books")
    reservations = relationship("Reservation", back_populates="book")
    loans = relationship("Loan", back_populates="book")


class Reservation(Base):
    __tablename__ = "reservation"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("book.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    reservation_date = Column(Date, nullable=False)
    reservation_status = Column(Integer, nullable=0)
    created_at = Column(DateTime, nullable=False, default=func.current_timestamp())
    updated_at = Column(DateTime, nullable=False, default=func.current_timestamp(), onupdate=func.current_timestamp())
    is_valid = Column(Boolean, nullable=False, default=True)

    book = relationship("Book", back_populates="reservations")
    user = relationship("User", back_populates="reservations")


class Loan(Base):
    __tablename__ = "loan"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("book.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    loan_date = Column(Date, nullable=False)
    due_date = Column(Date, nullable=False)
    extend_status = Column(Boolean, nullable=False, default=False)
    return_status = Column(Boolean, nullable=False, default=False)
    return_date = Column(Date)
    overdue_days = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, nullable=False, default=func.current_timestamp())
    updated_at = Column(DateTime, nullable=False, default=func.current_timestamp(), onupdate=func.current_timestamp())
    is_valid = Column(Boolean, nullable=False, default=True)

    book = relationship("Book", back_populates="loans")
    user = relationship("User", back_populates="loans")


class LibrarySetting(Base):
    __tablename__ = "library_setting"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    value = Column(String(50), nullable=False)
    data_type = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, default=func.current_timestamp())
    updated_at = Column(DateTime, nullable=False, default=func.current_timestamp(), onupdate=func.current_timestamp())
    is_valid = Column(Boolean, nullable=False, default=True)


class BookStat(Base):
    __tablename__ = 'book_stat'

    book_info_id = Column(Integer, ForeignKey('book_info.id'), primary_key=True)
    review_count = Column(Integer)
    loan_count = Column(Integer)

    book_info = relationship("BookInfo", viewonly=True)
