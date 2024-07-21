from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
from contextlib import contextmanager
from typing import Generator
from core.config import Settings

settings = Settings()


class DatabaseConnection:
    def __init__(self):
        self.SQLALCHEMY_DATABASE_URL = self._get_database_url()
        print(f"Database URL: {self.SQLALCHEMY_DATABASE_URL}")
        print(f"Database URL: {self.SQLALCHEMY_DATABASE_URL}")
        print(f"Database URL: {self.SQLALCHEMY_DATABASE_URL}")
        print(f"Database URL: {self.SQLALCHEMY_DATABASE_URL}")
        print(f"Database URL: {self.SQLALCHEMY_DATABASE_URL}")
        print(f"Database URL: {self.SQLALCHEMY_DATABASE_URL}")
        print(f"Database URL: {self.SQLALCHEMY_DATABASE_URL}")
        print(f"Database URL: {self.SQLALCHEMY_DATABASE_URL}")
        print(f"Database URL: {self.SQLALCHEMY_DATABASE_URL}")
        print(f"Database URL: {self.SQLALCHEMY_DATABASE_URL}")
        print(f"Database URL: {self.SQLALCHEMY_DATABASE_URL}")
        print(f"Database URL: {self.SQLALCHEMY_DATABASE_URL}")
        print(f"Database URL: {self.SQLALCHEMY_DATABASE_URL}")
        self.engine = create_engine(
            self.SQLALCHEMY_DATABASE_URL,
            pool_recycle=500,
            pool_pre_ping=True,
            connect_args={"connect_timeout": 100}
        )
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def _get_database_url(self) -> str:
        if settings.ENVIRONMENT in ["development", "production"]:
            return f"mysql+pymysql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
        elif settings.ENVIRONMENT == "exp":
            raise NotImplementedError("Experimental environment not supported yet")
        else:
            raise ValueError(f"Unknown environment: {settings.ENVIRONMENT}")

    @contextmanager
    def get_db_session(self) -> Generator[Session, None, None]:
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise
        finally:
            session.close()


db = DatabaseConnection()


def get_db() -> Generator[Session, None, None]:
    with db.get_db_session() as session:
        yield session
