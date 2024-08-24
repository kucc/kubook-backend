from books.schemas import models, schemas
from sqlalchemy.orm import Session

from models import Book, BookCategory, BookInfo


def search_books(db: Session, search_query: str):
    pass


def get_books_by_category(db: Session, category_id: int):
    pass
