# 🛠️ 음성 복제 프로젝트 (Voice-Clone Project)

> **데이터 엔지니어링과 웹 서비스를 위한 실무 수준의 인프라 구축**

---

## 🚀 프로젝트 개요

이 레포지토리는 음성 복제 프로젝트(Voice-Clone)를 위한 실무 수준의 인프라 구성을 담고 있습니다. GitHub Actions를 활용한 CI/CD 자동화, 모니터링 솔루션 (Airflow, Prometheus, cAdvisor, Grafana), 그리고 Let's Encrypt 기반 SSL 설정을 포함합니다.

---

## 🌐 구성 요소 및 인프라

| 서비스           | URL                                                 | 설명                          |
|----------------|-----------------------------------------------------|-------------------------------|
| **메인 API**     | [www.byhyeon.com](https://www.byhyeon.com)         | FastAPI 메인 서비스            |
| **Airflow**     | [airflow.byhyeon.com](https://airflow.byhyeon.com) | 워크플로우 관리 (ETL 파이프라인)  |
| **Grafana**     | [grafana.byhyeon.com](https://grafana.byhyeon.com) | 데이터 시각화 및 대시보드        |
| **Prometheus**  | [prometheus.byhyeon.com](https://prometheus.byhyeon.com) | 시스템 및 애플리케이션 메트릭    |
| **cAdvisor**    | [cadvisor.byhyeon.com](https://cadvisor.byhyeon.com) | 도커 컨테이너 메트릭           |

---

## 🗃️ 데이터베이스 및 스토리지

- **AWS S3** : 클라우드 파일 저장소
- **PostgreSQL** : 로컬 서버 설치, 데이터베이스 관리

---

## 🖥️ 시스템 사양

- **CPU**: Intel i5-6600 (4코어)
- **RAM**: 16GB
- **저장 장치**: 500GB SSD

---

## 🔐 보안 설정

- Let's Encrypt를 통한 HTTPS/SSL 적용 (자동 갱신)
- Nginx Reverse Proxy로 서브도메인 라우팅
- 민감한 모니터링 서비스에 Basic 인증 적용 (Prometheus, cAdvisor)

---

## ⚙️ CI/CD 자동화

- GitHub Actions를 통한 자동 배포
- Docker Compose를 통한 서비스 관리
- 장애 발생 시 자동 재시작 구성

---


---

## 🖥️ 모니터링 및 알림 설정

- Grafana 대시보드를 통해 Prometheus와 cAdvisor 메트릭 통합
- CPU, 메모리, 디스크 사용량 및 Docker 컨테이너 실시간 메트릭 제공
- Grafana를 통한 알림 설정 가능

---

## 💻 배포 방법

1. GitHub 저장소 클론
2. 환경 설정 및 권한 설정
3. Docker Compose를 통해 서비스 실행
4. Nginx 및 SSL 설정

---

## ✅ 상태 확인 방법

- Docker 컨테이너 상태 점검
- SSL 인증서 자동 갱신 상태 확인

---

## 📈 향후 개선사항


---