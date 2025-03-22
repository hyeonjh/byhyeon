# aws_conn.py

import os
import boto3

# AWS 자격 증명과 리전을 환경 변수로 설정
def get_s3_client():
    # 환경 변수에서 AWS 자격 증명 읽기
    s3_client = boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_REGION')
    )
    return s3_client

# 버킷 이름을 한 번만 설정
def get_bucket_name():
    return os.getenv('S3_BUCKET_NAME')  # 환경 변수에서 S3 버킷 이름 가져오기
