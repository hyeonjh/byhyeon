# 🗣️ Voice Clone 프로젝트

이 프로젝트는 **음성 복제 기반 음성 생성 서비스**입니다.  
 누구나 쉽게 개발 환경을 구성하고, GitHub Actions를 활용한 자동 배포까지 연동할 수 있습니다.

---

## 🐳 Docker 권한 설정 (중요)

`docker` 명령어를 사용하려면, 현재 계정을 Docker 그룹에 추가해야 합니다.  
이를 위해 아래 셋업 스크립트에서 자동으로 설정되며, **한 번만 재접속하면** 권한이 적용됩니다.

---

## 1️⃣ 개발 환경 자동 세팅 (`setup.sh`)

Ubuntu에서 아래 명령어를 입력하면 개발에 필요한 모든 환경이 자동으로 구성됩니다:

```bash
# 1. GitHub에서 프로젝트 클론
# 초기 시스템 셋업
sudo apt update
sudo apt install -y git

git clone https://github.com/hyeonjh/voice-clone.git
cd voice-clone

# 2. 셋업 스크립트 실행
chmod +x setup.sh
./setup.sh
```


## 2️⃣ 터미널 재시작 (중요)

셋업 완료 후에는 아래 명령어로 **터미널을 종료하고 다시 실행**해주세요:

```bash
exit
```

다시 Ubuntu를 실행한 후, 아래 명령어로 컨테이너를 실행합니다:

```bash

cd ~/voice-clone

systemctl start docker
docker-compose up -d --build
```

---

## 3️⃣ 프로젝트 실행 확인

```bash
docker ps
```

→ `voice-clone`이라는 컨테이너가 **Up** 상태인지 확인

웹 브라우저에서 확인:

```
http://localhost:8000
```

→ FastAPI 앱이 열리면 성공 🎉

---

## 4️⃣ GitHub Actions Self-Hosted Runner 설치 (선택)

자동 배포(CI/CD)를 위해 GitHub Actions runner를 **Ubuntu**에 설치할 수 있습니다.  
이 작업은 선택 사항이며, **1회만 수행하면 됩니다.**

```bash
# 1. Runner 디렉토리 생성
mkdir actions-runner && cd actions-runner

# 2. Runner 패키지 다운로드
curl -o actions-runner-linux-x64-2.323.0.tar.gz -L https://github.com/actions/runner/releases/download/v2.323.0/actions-runner-linux-x64-2.323.0.tar.gz

# 3. 압축 해제
tar xzf actions-runner-linux-x64-2.323.0.tar.gz

# 4. GitHub에서 발급한 토큰으로 설정
./config.sh --url https://github.com/hyeonjh/voice-clone --token <YOUR_TOKEN>

# 5. Runner 실행
# ./run.sh

# 백그라운드 실행 + 로그 저장
nohup ./run.sh > ~/runner.log 2>&1 &

# 로그 보기
tail -f ~/runner.log

# 중지
pkill -f run.sh
```

---

## 📁 프로젝트 구조 

```
VOICE-CLONE/
├── .github/
│   └── workflows/
│       └── deploy.yml
├── airflow/
│   ├── dags/
│   │   └── local_s3_transfer_dag.py
│   └── task/
│       ├── aws_conn.py
│       ├── download_from_s3.py
│       └── upload_to_s3.py
├── .dockerignore
├── .gitignore
├── docker-compose.yml
├── requirements.txt
├── Dockerfile
├── main.py
├── README.md
└── setup.sh

```

---

## 🙌 문의 및 피드백

프로젝트나 셋업 과정에 대한 질문은 GitHub Issues로 남겨주세요!  
더 나은 자동화 환경을 함께 만들어가요 😄
