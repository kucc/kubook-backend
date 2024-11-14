from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import Settings
from routes.admin.admin_books_route import router as admin_books_router
from routes.admin.notice_route import router as admin_notice_router
from routes.authentication_route import router as auth_router
from routes.book_review_route import router as review_router
from routes.bookrequest_route import router as bookrequest_router
from routes.books_route import router as books_router
from routes.loan_route import router as loan_router
from routes.notice_route import router as notice_router
from routes.user_route import router as user_router

settings = Settings()

app = FastAPI(
    title="쿠책책 API 서버",
    description="쿠책책 API 서버입니다.",
    version="0.1.0",
    contact={
        "name": "Minjae",
        "url": "https://github.com/mjkweon17",
        "email": "mjkweon17@korea.ac.kr"
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT"
    }
)

# CORS
origins = [
    "http://localhost:10242",
    "http://localhost:5173"
    "http://localhost:3000",
    "http://localhost:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(auth_router)
app.include_router(admin_books_router)
app.include_router(books_router)
app.include_router(user_router)
app.include_router(loan_router)
app.include_router(review_router)
app.include_router(bookrequest_router)
app.include_router(admin_notice_router)
app.include_router(notice_router)


@app.get("/")
async def root():
    return {"message": "쿠책책 API 서버입니다!"}
