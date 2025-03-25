# Base image
FROM python:3.9-slim

# 작업 디렉토리 설정
WORKDIR /app

# pip 업그레이드 먼저
RUN pip install --upgrade pip

# requirements.txt 복사 및 패키지 설치
COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r requirements.txt && pip install --no-cache-dir "email-validator>=2.0"
# 나머지 앱 파일 복사
COPY . .

# FastAPI 앱 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
