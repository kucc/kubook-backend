from .base import Base
from sqlalchemy import Boolean, Column, Integer, String, DateTime
from sqlalchemy.sql import func


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    auth_id = Column(String(50), unique=True, nullable=False)
    user_name = Column(String(45), nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    email = Column(String(100), unique=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.current_timestamp())
    updated_at = Column(DateTime, nullable=False, default=func.current_timestamp(), onupdate=func.current_timestamp())
    is_valid = Column(Boolean, nullable=False, default=True)
