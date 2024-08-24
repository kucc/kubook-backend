from sqlalchemy import (TIMESTAMP, Boolean, Column, Date, Enum, ForeignKey,
                        Integer)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from domain.enums.admin_status import AdminStatus

from .base import Base


class Admin(Base):
    __tablename__ = "admin"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    # TODO: 현재 AdminStatus가 class AdminStatus(str, Enum)이 아니라 조금 복잡한 구조인데 잘되는지 확인해야 함...
    admin_status = Column(Enum(AdminStatus), nullable=False)
    expiration_date = Column(Date, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False,
                        default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, nullable=False, default=func.current_timestamp(
    ), onupdate=func.current_timestamp())
    is_deleted = Column(Boolean, nullable=False, default=True)

    user = relationship("User", back_populates="admin")
    notices = relationship("Notice", back_populates="admin")
