from .base import Base


class BookStat(Base):
    __tablename__ = 'book_stat'

    book_info_id = Column(Integer, ForeignKey('book_info.id'), primary_key=True)
    review_count = Column(Integer)
    loan_count = Column(Integer)

    book_info = relationship("BookInfo", viewonly=True)
