from sqlalchemy import (BIGINT, TIMESTAMP, BigInteger, Boolean, Column,
                        Integer, String)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .base import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    auth_id = Column(String(255), nullable=False)
    auth_type = Column(String(20), nullable=False, default="FIREBASE")
    email = Column(String(100), nullable=False)
    user_name = Column(String(45), nullable=False)
    is_active = Column(String(20), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now())
    is_deleted = Column(Boolean, nullable=False, default=False)

    admin = relationship("Admin", back_populates="user")
    requested_books = relationship("RequestedBook", back_populates="user")
    loans = relationship("Loan", back_populates="user")
    book_reviews = relationship("BookReview", back_populates="user")
    notices = relationship("Notice", back_populates="user")
