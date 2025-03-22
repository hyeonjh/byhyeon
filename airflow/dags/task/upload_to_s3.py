import os
import boto3

def upload_m4a_to_s3():
    local_dir = '/mnt/d/voice/upload'
    bucket_name = '형-s3-버킷'
    s3_prefix = 'uploaded-audio/'

    s3 = boto3.client('s3', aws_access_key_id='형-key', aws_secret_access_key='형-secret')

    for filename in os.listdir(local_dir):
        if filename.endswith('.m4a'):
            local_path = os.path.join(local_dir, filename)
            s3_path = os.path.join(s3_prefix, filename)
            s3.upload_file(local_path, bucket_name, s3_path)
            print(f"✅ {filename} 업로드 완료 → s3://{bucket_name}/{s3_path}")