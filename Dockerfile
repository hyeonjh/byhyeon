# Base image
FROM python:3.9-slim

# `hyeonjh` 사용자 추가
RUN useradd -ms /bin/bash hyeonjh

# 작업 디렉토리 설정
WORKDIR /app  # 작업 디렉토리 설정

# pip 업그레이드 먼저
RUN pip install --upgrade pip

# requirements.txt 파일 복사
COPY requirements.txt .  # 로컬의 `requirements.txt`를 `/app`으로 복사

# 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt

# 나머지 파일을 모두 복사
COPY . .  # 현재 디렉토리의 모든 파일을 `/app`으로 복사

# 파일 소유자를 `hyeonjh`로 변경
RUN chown -R hyeonjh:hyeonjh /app  # `/app` 디렉토리 내 모든 파일의 소유자 변경

# 이후 모든 명령은 `hyeonjh` 사용자로 실행되도록 설정
USER hyeonjh

# FastAPI 앱 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
