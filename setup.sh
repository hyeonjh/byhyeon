#!/bin/bash

echo "📦 시스템 패키지 설치 중..."
sudo apt update
sudo apt install -y git zip unzip curl docker.io docker-compose

# Docker 그룹 권한 설정
sudo usermod -aG docker $USER

echo ""
echo "✅ 필수 패키지 설치 완료"
echo ""

echo "⚠️ 현재 터미널 세션에서는 Docker 권한이 아직 적용되지 않았습니다."
echo "👉 아래 순서대로 진행해주세요:"
echo ""
echo "1. WSL2 터미널을 종료하고 다시 실행하세요 (exit 입력 후 재접속)"
echo "2. 다음 명령어를 입력하여 컨테이너를 실행하세요:"
echo ""
echo "   cd ~/voice-clone"
echo "   docker-compose up -d --build"
echo ""
echo "🚀 그럼 http://localhost:8000 에서 서비스를 확인할 수 있습니다!"
echo ""

# setup.sh는 여기서 종료
exit 0