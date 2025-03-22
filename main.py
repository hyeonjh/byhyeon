from fastapi import FastAPI, UploadFile, File
import requests
import os

app = FastAPI()

# GitHub Secrets에서 불러오기 (환경 변수로)
AIRFLOW_TRIGGER_URL = os.getenv("AIRFLOW_TRIGGER_URL")
AIRFLOW_USERNAME = os.getenv("AIRFLOW_USERNAME")
AIRFLOW_PASSWORD = os.getenv("AIRFLOW_PASSWORD")

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = f"/tmp/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # DAG 트리거 (파일명 전달)
    response = requests.post(
        AIRFLOW_TRIGGER_URL,
        auth=(AIRFLOW_USERNAME, AIRFLOW_PASSWORD),
        json={"conf": {"filename": file.filename}},
        headers={"Content-Type": "application/json"},
    )

    return {
        "message": "업로드 요청 전송됨",
        "airflow_response": response.json()
    }
