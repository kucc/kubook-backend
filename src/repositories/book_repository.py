from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .base import Base


class Book(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True, index=True)
    book_info_id = Column(Integer, ForeignKey("book_info.id"), nullable=False)
    book_status = Column(String(20), nullable=False)
    note = Column(String(255), nullable=True)
    donor_name = Column(String(255), nullable=True)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP, nullable=False,
                        server_default=func.now(), onupdate=func.now())
    is_deleted = Column(Boolean, nullable=False, default=False)

    book_info = relationship("BookInfo", back_populates="books")
    loans = relationship("Loan", back_populates="book")
