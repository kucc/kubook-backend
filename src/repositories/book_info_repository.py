from sqlalchemy import (TIMESTAMP, Boolean, Column, Integer, SmallInteger,
                        String)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .base import Base


class BookInfo(Base):
    __tablename__ = "book_info"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    code = Column(String(20), nullable=False)
    category_name = Column(String(50), nullable=False)
    subtitle = Column(String(255), nullable=True)
    author = Column(String(100), nullable=False)
    publisher = Column(String(45), nullable=False)
    publication_year = Column(SmallInteger, nullable=False)
    image_url = Column(String(255), nullable=True)
    version = Column(String(45), nullable=True)
    major = Column(Boolean, nullable=True, default=False)
    language = Column(String(20), nullable=False, default="KOREAN")
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now())
    is_deleted = Column(Boolean, nullable=False, default=False)

    books = relationship("Book", back_populates="book_info")
    book_reviews = relationship("BookReview", back_populates="book_info")
