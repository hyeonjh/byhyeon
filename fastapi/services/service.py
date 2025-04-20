# FastAPI 관련
from fastapi import UploadFile, File
from fastapi.responses import JSONResponse

# 기타 외부 패키지
import openai
import boto3
import uuid
import hashlib
import os

# 내부 유틸 / 환경
from dotenv import load_dotenv
from logs.logs import logger
from db.insert import insert_row

from utils.s3 import get_s3_client, get_s3_bucket_name

s3 = get_s3_client()
bucket_name = get_s3_bucket_name()

load_dotenv()  # .env 파일에서 OPENAI_API_KEY 로드

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def handle_gpt(request):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "너는 파일 처리 도우미야."},
                {"role": "user", "content": request.prompt}
            ]
        ) 
        gpt_reply = response.choices[0].message.content
        return {"reply": gpt_reply}
    except Exception as e:
        return {"error": str(e)}

async def handle_upload(file: UploadFile):
    try:
        logger.info(f"📦 수신된 파일: {file.filename}")

        if not file.filename.lower().endswith((".wav", ".mp3", ".m4a")):
            logger.warning("⛔ 지원하지 않는 파일 확장자")
            return JSONResponse(
                status_code=400,
                content={"error": "지원하지 않는 파일 형식입니다."}
            )

        upload_uuid = uuid.uuid4()

         # ✅ 체크섬 먼저 계산
        hasher = hashlib.md5()
        while chunk := await file.read(8192):
            hasher.update(chunk)
        checksum = hasher.hexdigest()
        await file.seek(0)

        # ✅ DB insert 먼저 시도
        s3_folder = "uploads/"
        s3_filename = f"{upload_uuid}_{file.filename}"
        s3_key = f"{s3_folder}{s3_filename}"

        insert_row("metadata.s3_file_metadata", {
            "upload_uuid": str(upload_uuid),
            "original_filename": file.filename,
            "s3_folder_path": s3_folder,
            "s3_filename": s3_filename,
            "file_size": file.size,
            "file_type": file.content_type,
            "checksum": checksum
        })

        # ✅ insert 성공했으면 → S3 업로드
        s3.upload_fileobj(
            Fileobj=file.file,
            Bucket=bucket_name,
            Key=s3_key
        )
        logger.info(f"✅ S3 업로드 성공: {s3_filename}")

        return {
            "upload_uuid": str(upload_uuid),
            "status": "uploaded"
        }

    except ValueError as ve:
        if "중복된 파일입니다" in str(ve):
            logger.warning(f"⛔ 중복 업로드 차단: {file.filename}")
            return JSONResponse(
                status_code=409,
                content={"status": "duplicate", "detail": str(ve)}
            )
        else:
            logger.error(f"❌ 처리 중 ValueError: {ve}", exc_info=True)
            return {"error": str(ve)}

    except Exception as e:
        logger.error(f"❌ 업로드 실패: {e}", exc_info=True)
        return {"error": str(e)}
