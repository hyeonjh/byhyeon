# Base image
FROM python:3.9-slim

# 사용자 `hyeonjh` 추가
RUN useradd -ms /bin/bash hyeonjh

# 작업 디렉토리 설정 (디렉토리가 없으면 생성)
RUN mkdir -p /app
WORKDIR /app  # 작업 디렉토리 설정

# pip 업그레이드 먼저
RUN pip install --upgrade pip

# requirements.txt 복사 및 패키지 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 나머지 파일을 복사하고 권한 수정 (파일 소유자 변경)
COPY . .

# 파일 소유자를 `hyeonjh`로 변경
RUN chown -R hyeonjh:hyeonjh /app

# 이후 모든 명령은 `hyeonjh` 사용자로 실행되도록 설정
USER hyeonjh

# uvicorn으로 FastAPI 앱 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
