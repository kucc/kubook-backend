from .base import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, DateTime, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Admin(Base):
    __tablename__ = "admin"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    admin_status = Column(Boolean, nullable=False)
    expiration_date = Column(Date, nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.current_timestamp())
    updated_at = Column(DateTime, nullable=False, default=func.current_timestamp(), onupdate=func.current_timestamp())
    is_valid = Column(Boolean, nullable=False, default=False)

    user = relationship("User", back_populates="admin")
    notices = relationship("Notice", back_populates="admin")
