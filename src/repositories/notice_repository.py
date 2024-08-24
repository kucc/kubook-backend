from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.sql import func

from .base import Base


class Notice(Base):
    __tablename__ = "notice"

    id = Column(Integer, primary_key=True, index=True)
    admin_id = Column(Integer, ForeignKey("admin.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, nullable=False, default=func.current_timestamp(), onupdate=func.current_timestamp())
    is_deleted = Column(Boolean, nullable=False, default=True)
