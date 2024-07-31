from .base import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, DateTime, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


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
