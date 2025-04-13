#!/bin/bash

echo "🚀 [1] Docker 네트워크(shared) 생성 중..."
docker network inspect shared >/dev/null 2>&1 || docker network create shared

echo "📁 [2] Airflow 디렉토리 준비 중..."
mkdir -p airflow/logs
mkdir -p airflow/plugins

echo "📝 [3] .env 파일 확인 중..."
if [ ! -f ".env" ]; then
  echo "AIRFLOW_UID=50000" > .env
  echo ".env 파일 생성 완료 ✅"
fi

echo "🐳 [4] docker-compose 서비스 실행 중..."
docker compose -f docker-compose-airflow.yml -f docker-compose-fastapi.yml -f docker-compose-monitoring.yml -f docker-compose-elk.yml up -d --build
echo "🎉 모든 서비스가 실행되었습니다!"
