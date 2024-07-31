from .base import Base
from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime, Boolean, func
from sqlalchemy.orm import relationship


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
