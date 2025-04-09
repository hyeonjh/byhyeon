# ✅ 수정된 FastAPI 코드
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from pydantic import BaseModel
import openai
import os
from dotenv import load_dotenv

load_dotenv()  # .env 파일에서 OPENAI_API_KEY 로드
openai.api_key = os.getenv("OPENAI_API_KEY")

class PromptRequest(BaseModel):
    prompt: str

app = FastAPI()  # ⛔ root_path 생략 또는 제거

@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <html>
        <head>
            <title>Monitoring Dashboard</title>
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
            </style>
        </head>
        <body>
            <h1>🔍 모니터링 도구 바로가기</h1>
            <a class="button" href="https://grafana.byhyeon.com" target="_blank">Grafana</a>
            <a class="button" href="https://prometheus.byhyeon.com" target="_blank">Prometheus</a>
            <a class="button" href="https://cadvisor.byhyeon.com" target="_blank">cAdvisor</a>
            <a class="button" href="https://airflow.byhyeon.com" target="_blank">Airflow</a>
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