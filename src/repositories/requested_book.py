from sqlalchemy import (TIMESTAMP, Boolean, Column, ForeignKey, Integer,
                        SmallInteger, String, Text)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .base import Base


class RequestedBook(Base):
    __tablename__ = "requested_book"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    book_title = Column(String(255), nullable=False)
    publication_year = Column(SmallInteger, nullable=True)
    reject_reason = Column(String(20), nullable=True)
    request_link = Column(String(255), nullable=False)
    reason = Column(Text, nullable=False)
    requested_at = Column(TIMESTAMP, nullable=False)
    processing_status = Column(String(20), nullable=False)
    processed_at = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now())
    is_deleted = Column(Boolean, nullable=False, default=False)

    user = relationship("User", back_populates="requested_books")
