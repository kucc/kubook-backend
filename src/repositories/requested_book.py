from .base import Base


class RequestedBook(Base):
    __tablename__ = "requested_book"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    book_title = Column(String(255), nullable=False)
    publication_year = Column(Integer)
    reject_reason = Column(Text, nullable=True)
    request_link = Column(String(100), nullable=False)
    reason = Column(Text, nullable=False)
    processing_status = Column(Integer, nullable=False, default=0)
    request_date = Column(Date, nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.current_timestamp())
    updated_at = Column(DateTime, nullable=False, default=func.current_timestamp(), onupdate=func.current_timestamp())
    is_valid = Column(Boolean, nullable=False, default=True)

    user = relationship("User", back_populates="requested_books")
