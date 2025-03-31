# # upload_to_s3.py

# import os
# from aws_conn import get_s3_client  # aws_conn.py에서 S3 클라이언트 가져오기
# from dotenv import load_dotenv

# load_dotenv()  

# def upload_m4a_to_s3(file_path, file_name):
#     s3_client = get_s3_client()  # S3 클라이언트를 한 번만 생성하여 가져오기
#     bucket_name = os.getenv('S3_BUCKET_NAME')  # 환경 변수에서 버킷 이름 가져오기
#     s3_client.upload_file(file_path, bucket_name, file_name)
#     print(f"✅ {file_name} S3에 업로드 완료")
