import os
import boto3

def download_m4a_from_s3():
    bucket_name = '형-s3-버킷'
    s3_prefix = 'uploaded-audio/'
    local_dir = '/mnt/d/voice/download'

    s3 = boto3.client('s3', aws_access_key_id='형-key', aws_secret_access_key='형-secret')

    objects = s3.list_objects_v2(Bucket=bucket_name, Prefix=s3_prefix)
    for obj in objects.get('Contents', []):
        filename = obj['Key'].split('/')[-1]
        if filename:
            s3.download_file(bucket_name, obj['Key'], os.path.join(local_dir, filename))
            print(f"✅ {filename} 다운로드 완료")