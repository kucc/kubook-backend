from .base import Base


class BookCategory(Base):
    __tablename__ = "book_category"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(5), nullable=False)
    name = Column(String(50), nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.current_timestamp())
    updated_at = Column(DateTime, nullable=False, default=func.current_timestamp(), onupdate=func.current_timestamp())
    is_valid = Column(Boolean, nullable=False, default=True)

    books = relationship("BookInfo", back_populates="category")
