from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

from task.aws_conn import get_s3_client, get_bucket_name

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

def test_s3_connection():
    s3 = get_s3_client()
    bucket = get_bucket_name()
    # 리스트만 해도 실제 연결 확인됨
    response = s3.list_objects_v2(Bucket=bucket)
    print(f"✅ S3 연결 성공! 버킷 '{bucket}'의 객체 수: {response.get('KeyCount', 0)}")

with DAG(
    dag_id='test_s3_connection_dag',
    default_args=default_args,
    start_date=datetime(2025, 1, 1),
    schedule_interval=None,  # 수동 실행 전용
    catchup=False,
    tags=['test', 's3']
) as dag:

    test_s3 = PythonOperator(
        task_id='check_s3_connection',
        python_callable=test_s3_connection
    )
