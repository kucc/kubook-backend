from .base import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, func
from sqlalchemy.orm import relationship


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
