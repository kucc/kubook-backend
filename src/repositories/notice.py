from .base import Base


class Notice(Base):
    __tablename__ = "notice"

    id = Column(Integer, primary_key=True, index=True)
    admin_id = Column(Integer, ForeignKey("admin.id"), nullable=False)
    user_id = Column(Integer)
    title = Column(String(255), nullable=False)
    notice_content = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.current_timestamp())
    updated_at = Column(DateTime, nullable=False, default=func.current_timestamp(), onupdate=func.current_timestamp())
    is_valid = Column(Boolean, nullable=False, default=True)

    admin = relationship("Admin", back_populates="notices")
