# ✅ 수정된 FastAPI 코드
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from pydantic import BaseModel
import openai
import os
from dotenv import load_dotenv

load_dotenv()  # .env 파일에서 OPENAI_API_KEY 로드
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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
             <br/><br/>
            <a class="button" href="/chat">💬 GPT 대화하기</a>
        </body>
    </html>
    """

# GPT 프롬프트 입력용 /chat 페이지
@app.get("/chat", response_class=HTMLResponse)
def chat_ui():
    return """
    <html>
        <head><title>GPT Chat</title></head>
        <body style="text-align: center; font-family: Arial; padding-top: 50px;">
            <h1>💬 GPT에게 질문하기</h1>
            <form onsubmit="event.preventDefault(); askGPT();">
                <input type="text" id="prompt" placeholder="질문을 입력하세요" style="width: 300px; padding: 8px;" />
                <button type="submit" style="padding: 8px 16px;">전송</button>
            </form>
            <div style="margin-top: 20px;">
                <strong>응답:</strong>
                <p id="response" style="white-space: pre-wrap;"></p>
            </div>
            <script>
                async function askGPT() {
                    const prompt = document.getElementById("prompt").value;
                    document.getElementById("response").innerText = "로딩 중...";
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