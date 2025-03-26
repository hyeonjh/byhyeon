FROM apache/airflow:2.7.2

COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

# ✅ entrypoint.sh 복사
COPY entrypoint.sh /opt/airflow/entrypoint.sh

USER root
RUN chmod +x /opt/airflow/entrypoint.sh
USER airflow