#!/bin/bash

echo "📦 Updating system & installing packages..."

# 시스템 업데이트 및 필수 패키지 설치
sudo apt update
sudo apt install -y git zip unzip curl docker.io docker-compose

# Docker 권한 설정 (재로그인 필요)
sudo usermod -aG docker $USER

echo "✅ 필수 패키지 설치 완료"

# (옵션) Docker 빌드 및 실행
if [ -f docker-compose.yml ]; then
  echo "🚀 docker-compose.yml 감지됨. 컨테이너 빌드 및 실행 중..."
  docker-compose up -d --build
else
  echo "⚠️ docker-compose.yml 파일이 없습니다. 수동으로 실행해 주세요."
fi
