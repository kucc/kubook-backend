from sqlalchemy.orm import relationship


from .base import Base
from .user import User


# User.requested_books = Base.relationship("RequestedBook", back_populates="user")
# User.admin = Base.relationship("Admin", back_populates="user", uselist=False)
# User.book_reviews = Base.relationship("BookReview", back_populates="user")
# User.reservations = Base.relationship("Reservation", back_populates="user")
# User.loans = Base.relationship("Loan", back_populates="user")
