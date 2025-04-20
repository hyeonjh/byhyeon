import boto3
import os

def get_s3_client():
    return boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION")
    )

def get_s3_bucket_name():
    return os.getenv("S3_BUCKET_NAME")

def upload_file_to_s3(file_obj, s3_key: str):
    bucket = get_s3_bucket_name()
    s3 = get_s3_client()
    s3.upload_fileobj(
        Fileobj=file_obj,
        Bucket=bucket,
        Key=s3_key
    )