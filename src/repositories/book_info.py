from .base import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, func
from sqlalchemy.orm import relationship


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
