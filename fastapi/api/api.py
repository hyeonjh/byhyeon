from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse ,HTMLResponse
from pydantic import BaseModel
from services.service import handle_upload, handle_gpt

router = APIRouter()

class PromptRequest(BaseModel):
    prompt: str

@router.post("/ask")
def ask_gpt(request: PromptRequest):
    return handle_gpt(request)

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    return await handle_upload(file)

@router.get("/", response_class=HTMLResponse)
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