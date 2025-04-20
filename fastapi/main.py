# main.py
from fastapi import FastAPI
from api.api import router as api_router
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

# 환경 변수 로드 (.env에서 API KEY, AWS 정보 등)
load_dotenv()

app = FastAPI()
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "https://byhyeon.com",
    "https://www.byhyeon.com"],
    allow_methods=["*"],
    allow_headers=["*"],
)