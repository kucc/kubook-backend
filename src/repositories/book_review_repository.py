from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .base import Base


class BookReview(Base):
    __tablename__ = "book_review"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    book_info_id = Column(Integer, ForeignKey("book_info.id"), nullable=False)
    review_content = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now())
    is_deleted = Column(Boolean, nullable=False, default=False)

    user = relationship("User", back_populates="book_reviews")
    book_info = relationship("BookInfo", back_populates="book_reviews")
