#!/bin/bash

echo "📦 Docker 및 필수 패키지 설치 중..."

# 기본 패키지
sudo apt update
sudo apt install -y ca-certificates curl gnupg zip unzip

# Docker 공식 GPG 키 추가
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Docker 공식 저장소 추가
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# 저장소 갱신 후 Docker 및 Compose 플러그인 설치
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# 현재 사용자에 Docker 그룹 권한 부여
sudo usermod -aG docker $USER

echo ""
echo "✅ Docker 및 필수 패키지 설치 완료"
echo ""

echo "⚠️ 현재 터미널 세션에서는 Docker 권한이 아직 적용되지 않았습니다."
echo "👉 아래 순서대로 진행해주세요:"
echo ""
echo "1. 터미널을 종료하고 다시 실행하세요 (exit 입력 후 재접속)"
echo "2. 다음 명령어를 입력하여 컨테이너를 실행하세요:"
echo ""
echo "   cd ~/voice-clone"
echo "   sudo systemctl start docker"
echo "   docker compose up -d --build"
echo ""
echo "🚀 그럼 http://localhost:8000 에서 서비스를 확인할 수 있습니다!"
echo ""

exit 0
