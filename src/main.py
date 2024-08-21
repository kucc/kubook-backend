from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import Settings
from routes.admin.book_request_route import router as admin_book_request_router
from routes.admin.book_route import router as admin_book_router
from routes.admin.loans_route import router as admin_loans_router
from routes.admin.notice_route import router as admin_notice_router
from routes.admin.reservation_route import router as admin_reservation_router
from routes.admin.route import router as admin_router
from routes.admin.setting_route import router as admin_setting_router
from routes.admin.user_route import router as admin_user_router
from routes.authentication_route import router as auth_router
from routes.book_request_route import router as book_request_router
from routes.book_route import router as book_router
from routes.food_route import router as food_router
from routes.food_order_route import router as food_order_router
from routes.loan_route import router as loan_router
from routes.reservation_route import router as reservation_router
from routes.review_route import router as review_router
from routes.test_route import router as test_router
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
    "http://localhost",
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

app.include_router(admin_book_request_router)
app.include_router(admin_book_router)
app.include_router(admin_loans_router)
app.include_router(admin_notice_router)
app.include_router(admin_reservation_router)
app.include_router(admin_router)
app.include_router(admin_setting_router)
app.include_router(admin_user_router)

app.include_router(auth_router)
app.include_router(book_request_router)
app.include_router(book_router)
app.include_router(loan_router)
app.include_router(reservation_router)
app.include_router(review_router)
app.include_router(test_router)
app.include_router(user_router)

app.include_router(food_router)
app.include_router(food_order_router)


@app.get("/")
async def root():
    return {"message": "쿠책책 API 서버입니다!"}
