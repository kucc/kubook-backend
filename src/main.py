from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

# from ssh import get_ssh_connection
from config import Settings

# from auth.router import router as auth_router
# from tests.test_router import router as test_router
# from admin.router import router as admin_router

settings = Settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    if settings.ENVIRONMENT == "development":
        # Open SSH Connection
        ssh_connection = get_ssh_connection()
        yield
        # Close SSH Connection
        ssh_connection.close()
    else:
        yield


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
    },
    lifespan=lifespan
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

# app.include_router(auth_router)
# app.include_router(test_router)
# app.include_router(admin_router)


@app.get("/")
async def root():
    return {"message": "쿠책책 API 서버입니다!"}
