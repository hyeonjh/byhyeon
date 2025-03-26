FROM apache/airflow:2.7.2

# 루트 권한으로 전환 (필요한 경우만)
USER root


# 필수 시스템 패키지 설치
RUN apt-get update && apt-get install -y \
    gcc \
    libxml2-dev \
    libxmlsec1-dev \
    pkg-config \
    libffi-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 권한 부여 (entrypoint.sh가 읽히게)
COPY entrypoint.sh /opt/airflow/entrypoint.sh
RUN chmod +x /opt/airflow/entrypoint.sh

# airflow 유저로 다시 돌아감
USER airflow

# requirements.txt 설치 (airflow 환경이 깨지지 않게 유저 airflow로 설치!)
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt
