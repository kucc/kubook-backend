from .base import Base
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship


class BookStat(Base):
    __tablename__ = 'book_stat'

    book_info_id = Column(Integer, ForeignKey('book_info.id'), primary_key=True)
    review_count = Column(Integer)
    loan_count = Column(Integer)

    book_info = relationship("BookInfo", viewonly=True)
