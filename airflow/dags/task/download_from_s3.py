# download_from_s3.py

import os
from aws_conn import get_s3_client, get_bucket_name  # aws_conn.py에서 S3 클라이언트와 버킷 이름 가져오기
from dotenv import load_dotenv

load_dotenv()  

def download_m4a_from_s3():
    s3_client = get_s3_client()  # S3 클라이언트를 한 번만 생성하여 가져오기
    bucket_name = get_bucket_name()  # aws_conn.py에서 한 번만 설정한 버킷 이름을 가져오기
    s3_prefix = 'uploaded-audio/'
    local_dir = '/mnt/d/voice/download'

    # S3 객체 리스트 가져오기
    objects = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=s3_prefix)
    for obj in objects.get('Contents', []):
        filename = obj['Key'].split('/')[-1]
        if filename:
            s3_client.download_file(bucket_name, obj['Key'], os.path.join(local_dir, filename))
            print(f"✅ {filename} 다운로드 완료")
