from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from task.upload_to_s3 import upload_m4a_to_s3
from task.download_from_s3 import download_m4a_from_s3

with DAG(
    dag_id='local_s3_transfer_dag',
    start_date=datetime(2024, 1, 1),
    schedule_interval='@once',  # 수동 실행 or 테스트용
    catchup=False
) as dag:

    upload_task = PythonOperator(
        task_id='upload_m4a_to_s3',
        python_callable=upload_m4a_to_s3
    )

    download_task = PythonOperator(
        task_id='download_m4a_from_s3',
        python_callable=download_m4a_from_s3
    )

    upload_task >> download_task
