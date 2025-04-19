# FastAPI 관련
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel

import openai

# 환경변수
import os
from dotenv import load_dotenv


# 외부 API / 클라우드
import openai
import boto3

# 유틸리티
import uuid
import hashlib

#insert db 
from db.insert import insert_row 

# 로그설정
from logs.logs import logger

load_dotenv()  # .env 파일에서 OPENAI_API_KEY 로드
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION")
)
bucket_name = os.getenv("S3_BUCKET_NAME")




class PromptRequest(BaseModel):
    prompt: str

app = FastAPI()  # ⛔ root_path 생략 또는 제거

@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <html>
        <head>
            <title>Monitoring + GPT</title>
            <style>
                body { font-family: Arial; text-align: center; padding-top: 50px; background-color: #f5f5f5; }
                h1 { color: #333; }
                a.button {
                    display: inline-block;
                    padding: 12px 24px;
                    margin: 10px;
                    font-size: 16px;
                    background-color: #007bff;
                    color: white;
                    text-decoration: none;
                    border-radius: 8px;
                }
                a.button:hover {
                    background-color: #0056b3;
                }
                #gpt-box {
                    margin-top: 40px;
                    padding: 20px;
                    background-color: #ffffff;
                    border-radius: 10px;
                    box-shadow: 0 0 10px rgba(0,0,0,0.1);
                    width: 500px;
                    margin-left: auto;
                    margin-right: auto;
                }
                input[type="text"] {
                    width: 80%;
                    padding: 10px;
                    font-size: 16px;
                }
                button {
                    padding: 10px 20px;
                    font-size: 16px;
                    margin-left: 10px;
                }
                #response {
                    margin-top: 20px;
                    white-space: pre-wrap;
                    color: #333;
                }
            </style>
        </head>
        <body>
            <h1>🔍 모니터링 도구 바로가기</h1>
            <a class="button" href="https://grafana.byhyeon.com" target="_blank">Grafana</a>
            <a class="button" href="https://prometheus.byhyeon.com" target="_blank">Prometheus</a>
            <a class="button" href="https://cadvisor.byhyeon.com" target="_blank">cAdvisor</a>
            <a class="button" href="https://airflow.byhyeon.com" target="_blank">Airflow</a>
            <a class="button" href="https://kibana.byhyeon.com/app/home#/" target="_blank">Kibana</a>

            <div id="gpt-box">
                <h2>💬 GPT에게 바로 질문하기</h2>
                <form onsubmit="event.preventDefault(); askGPT();">
                    <input type="text" id="prompt" placeholder="질문을 입력하세요" />
                    <button type="submit">전송</button>
                </form>
                <div id="response"></div>
            </div>

            <script>
                async function askGPT() {
                    const prompt = document.getElementById("prompt").value;
                    document.getElementById("response").innerText = "GPT 응답 중...";
                    const response = await fetch("/ask", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({ prompt })
                    });
                    const data = await response.json();
                    document.getElementById("response").innerText = data.reply || data.error;
                }
            </script>
        </body>
    </html>
    """

@app.post("/ask")
def ask_gpt(request: PromptRequest):
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
    

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        logger.info(f"📦 수신된 파일: {file.filename}")

        # ✅ 1. 파일 확장자 제한 (선택)
        if not file.filename.lower().endswith((".wav", ".mp3", ".m4a")):
            logger.warning("⛔ 지원하지 않는 파일 확장자")
            return JSONResponse(
                status_code=400,
                content={"error": "지원하지 않는 파일 형식입니다."}
            )

        # ✅ 2. UUID 생성
        upload_uuid = uuid.uuid4()

        # ✅ 3. 체크섬 계산
        hasher = hashlib.md5()
        while chunk := await file.read(8192):
            hasher.update(chunk)
        checksum = hasher.hexdigest()

        # ✅ 4. 스트림 리셋
        await file.seek(0)

        # ✅ 5. S3 업로드 경로 설정
        s3_folder = "uploads/"
        s3_filename = f"{upload_uuid}_{file.filename}"
        s3_key = f"{s3_folder}{s3_filename}"

        # ✅ 6. S3 업로드
        s3.upload_fileobj(
            Fileobj=file.file,
            Bucket=bucket_name,
            Key=s3_key
        )
        logger.info(f"✅ S3 업로드 성공: {s3_filename}")

        # ✅ 7. 메타데이터 기록
        insert_row("metadata.s3_file_metadata", {
            "upload_uuid": str(upload_uuid),
            "original_filename": file.filename,
            "s3_folder_path": s3_folder,
            "s3_filename": s3_filename,
            "file_size": file.size,
            "file_type": file.content_type,
            "checksum": checksum
        })

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