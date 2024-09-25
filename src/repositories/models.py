from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func

Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    auth_id = Column(String(255), nullable=False)
    auth_type = Column(String(20), nullable=False, default="FIREBASE")
    email = Column(String(100), nullable=False)
    user_name = Column(String(45), nullable=False)
    is_active = Column(Boolean, nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.current_timestamp())
    updated_at = Column(DateTime, nullable=False, default=func.current_timestamp(), onupdate=func.current_timestamp())
    is_deleted = Column(Boolean, nullable=False, default=False)

    # Relationships
    admin = relationship("Admin", back_populates="user")
    requested_books = relationship("RequestedBook", back_populates="user")
    loans = relationship("Loan", back_populates="user")
    book_reviews = relationship("BookReview", back_populates="user")
    food_orders = relationship("FoodOrder", back_populates="user")


class Admin(Base):
    __tablename__ = "admin"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    admin_status = Column(Boolean, nullable=False)
    expiration_date = Column(Date, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    is_deleted = Column(Boolean, nullable=False, default=False)

    # Relationship
    user = relationship("User", back_populates="admin")


class RequestedBook(Base):
    __tablename__ = "requested_book"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    book_title = Column(String(255), nullable=False)
    publication_year = Column(Integer)
    reject_reason = Column(String(20))
    request_link = Column(String(255), nullable=False)
    reason = Column(String, nullable=False)
    requested_at = Column(DateTime, nullable=False)
    processing_status = Column(Integer, nullable=False)
    processed_at = Column(DateTime)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    is_deleted = Column(Boolean, nullable=False, default=False)

    # Relationship
    user = relationship("User", back_populates="requested_books")


class Loan(Base):
    __tablename__ = "loan"

    id = Column(Integer, primary_key=True, autoincrement=True)
    book_id = Column(Integer, ForeignKey("book.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    loan_date = Column(DateTime, nullable=False)
    due_date = Column(DateTime, nullable=False)
    extend_status = Column(Boolean, nullable=False, default=False)
    return_status = Column(Boolean, nullable=False, default=False)
    return_date = Column(DateTime)
    overdue_days = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    is_deleted = Column(Boolean, nullable=False, default=False)

    # Relationships
    user = relationship("User", back_populates="loans")
    book = relationship("Book", back_populates="loans")


class BookReview(Base):
    __tablename__ = "book_review"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    book_info_id = Column(Integer, ForeignKey("book_info.id"), nullable=False)
    review_content = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    is_deleted = Column(Boolean, nullable=False, default=False)

    # Relationships
    user = relationship("User", back_populates="book_reviews")
    book_info = relationship("BookInfo", back_populates="book_reviews")


class BookInfo(Base):
    __tablename__ = "book_info"

    id = Column(Integer, primary_key=True, autoincrement=True)
    book_title = Column(String(255), nullable=False)
    code = Column(String(20), nullable=False)
    category_name = Column(String(50), nullable=False)
    subtitle = Column(String(255))
    author = Column(String(100), nullable=False)
    publisher = Column(String(45), nullable=False)
    publication_year = Column(Integer, nullable=False)
    image_url = Column(String(255))
    version = Column(String(45))
    major = Column(Boolean, default=False)
    language = Column(String(20), nullable=False, default="KOREAN")
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    is_deleted = Column(Boolean, nullable=False, default=False)

    # Relationships
    book_reviews = relationship("BookReview", back_populates="book_info")
    books = relationship("Book", back_populates="book_info")


class Book(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True, autoincrement=True)
    book_info_id = Column(Integer, ForeignKey("book_info.id"), nullable=False)
    book_status = Column(String(20), nullable=False)
    note = Column(String(255))
    donor_name = Column(String(255))
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    is_deleted = Column(Boolean, nullable=False, default=False)

    # Relationships
    book_info = relationship("BookInfo", back_populates="books")
    loans = relationship("Loan", back_populates="book")


class Notice(Base):
    __tablename__ = "notice"

    id = Column(Integer, primary_key=True, autoincrement=True)
    admin_id = Column(Integer, ForeignKey("admin.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.current_timestamp())
    updated_at = Column(DateTime, nullable=False, default=func.current_timestamp(), onupdate=func.current_timestamp())
    is_deleted = Column(Boolean, nullable=False, default=False)
    # Relationships
    admin = relationship("Admin", foreign_keys=[admin_id])
    user = relationship("User", foreign_keys=[user_id])
