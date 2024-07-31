import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')

load_dotenv(dotenv_path)


class Settings(BaseSettings):
    # 환경 설정
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

    # 데이터베이스 설정
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: int = int(os.getenv("DB_PORT", 3306))
    DB_NAME: str = os.getenv("DB_NAME", "library_db")
    DB_USER: str = os.getenv("DB_USER", "root")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "password")

    # JWT 토큰 설정
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "your-secret-key")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_ACCESS_EXPIRATION_TIME_MINUTES: int = int(os.getenv("JWT_ACCESS_EXPIRATION_TIME_MINUTES", 30))
    JWT_REFRESH_EXPIRATION_TIME_MINUTES: int = int(os.getenv("JWT_REFRESH_EXPIRATION_TIME_MINUTES", 60))

    # 애플리케이션 설정
    APP_TITLE: str = "Library Management System"
    APP_DESCRIPTION: str = "API for managing library resources"
    APP_VERSION: str = "0.1.0"

    # Firebase 설정
    FIREBASE_SERVICE_ACCOUNT_KEY: str = os.getenv("FIREBASE_SERVICE_ACCOUNT_KEY", "firebase-service-account-key.json")
    FIREBASE_WEB_API_KEY: str = os.getenv("FIREBASE_WEB_API_KEY", "firebase-web-api-key")

    # 임시 사용자 이름
    TEMP_USER_NAME: str = os.getenv("TEMP_USER_NAME", "임시 사용자")
