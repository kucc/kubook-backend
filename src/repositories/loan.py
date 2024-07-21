from .base import Base


class Loan(Base):
    __tablename__ = "loan"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("book.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    loan_date = Column(Date, nullable=False)
    due_date = Column(Date, nullable=False)
    extend_status = Column(Boolean, nullable=False, default=False)
    return_status = Column(Boolean, nullable=False, default=False)
    return_date = Column(Date)
    overdue_days = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, nullable=False, default=func.current_timestamp())
    updated_at = Column(DateTime, nullable=False, default=func.current_timestamp(), onupdate=func.current_timestamp())
    is_valid = Column(Boolean, nullable=False, default=True)

    book = relationship("Book", back_populates="loans")
    user = relationship("User", back_populates="loans")
