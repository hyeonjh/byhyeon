# 🗣️ Voice Clone 프로젝트

이 프로젝트는 **음성 복제 기반 음성 생성 서비스**입니다.  
WSL2 환경에서 누구나 쉽게 개발 환경을 구성하고, GitHub Actions를 활용한 자동 배포까지 연동할 수 있습니다.

---

## 1️⃣ WSL2 개발 환경 자동 세팅 (`setup.sh`)

WSL2 Ubuntu에서 아래 명령어를 입력하면 개발에 필요한 모든 환경이 자동으로 구성됩니다:

```bash
# 1. 프로젝트 클론
git clone https://github.com/hyeonjh/voice-clone.git
cd voice-clone

# 2. 셋업 스크립트 실행
chmod +x setup.sh
./setup.sh
```

### ✅ `setup.sh`가 수행하는 작업

- 📦 **필수 패키지 설치**:
  - `zip`, `unzip`, `curl`
  - `docker`, `docker-compose`
- ⚙️ **`docker-compose.yml` 파일이 존재할 경우**:
  - Docker 이미지 자동 빌드
  - 컨테이너 자동 실행

---

## 2️⃣ 프로젝트 실행 확인

```bash
docker ps
```

컨테이너가 실행되고 있는지 확인하세요.  
웹 서비스가 있는 경우, `http://localhost:8000` 등으로 접근해 확인할 수 있습니다.

---

## 3️⃣ GitHub Actions Self-Hosted Runner 설치 (선택)

자동 배포(CI/CD)를 위해 GitHub Actions runner를 **로컬 WSL2**에 설치할 수 있습니다.  
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
./run.sh
```

> 🔐 `YOUR_TOKEN`은 GitHub → **Settings → Actions → Runners → New self-hosted runner** 메뉴에서 발급 가능합니다.  
> 💡 `./run.sh`는 계속 실행 중이어야 Actions가 동작합니다. `tmux`, `screen`, 또는 `./svc.sh install`로 백그라운드 실행도 가능합니다.

---

## 📁 프로젝트 구조
```
voice-clone/
├── .github/
│   └── workflows/
│       └── deploy.yml
├── setup.sh
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── main.py
├── README.md
```

---

## 🙌 문의 및 피드백

프로젝트나 셋업 과정에 대한 질문은 GitHub Issues로 남겨주세요!  
더 나은 자동화 환경을 함께 만들어가요 😄
