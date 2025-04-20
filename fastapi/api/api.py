from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse ,HTMLResponse
from pydantic import BaseModel
from services.service import handle_upload, handle_gpt
from typing import List

router = APIRouter()

class PromptRequest(BaseModel):
    prompt: str

@router.post("/ask")
def ask_gpt(request: PromptRequest):
    return handle_gpt(request)

@router.post("/upload")
async def upload(files: List[UploadFile] = File(...)):
    results = []
    for file in files:
        result = await handle_upload(file)
        results.append({file.filename: result})
    return {"files": results}

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

            <hr style="margin: 40px 0;">

            <h2>💬 GPT에게 업로드 여부 묻기</h2>
            <form onsubmit="event.preventDefault(); askGPT();">
                <input type="text" id="prompt" placeholder="GPT에게 질문" />
                <button type="submit">질문 보내기</button>
            </form>

            <input type="file" id="uploadInput" multiple />
            <div id="response" style="margin-top:10px;"></div>
            <div id="upload-result" style="margin-top:20px; white-space: pre-wrap;"></div>

            <script>
                async function askGPT() {
                    const prompt = document.getElementById("prompt").value;
                    const files = document.getElementById("uploadInput").files;
                    const fileNames = Array.from(files).map(f => f.name).join(", ");
                    const fullPrompt = `
                    당신은 파일 업로드 여부를 판단하는 AI입니다.
                    파일 목록을 분석하여 업로드가 필요한 경우에는 "업로드하세요",
                    필요하지 않은 경우에는 "업로드하지 마세요" 라고만 답하세요.
                    그 외의 말은 하지 마세요.

                    파일 목록: ${fileNames}
                    `;

                    document.getElementById("response").innerText = "GPT 응답 중...";

                    const response = await fetch("/ask", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({ prompt: fullPrompt })
                    });

                    const data = await response.json();
                    const reply = data.reply || data.error;
                    document.getElementById("response").innerText = reply;

                    // ✅ GPT가 업로드 허용한 경우 자동 업로드 실행
                    if (reply.includes("업로드") && reply.includes("하세요")) {
                        uploadFiles();
                    }
                }

                async function uploadFiles() {
                    const input = document.getElementById("uploadInput");
                    const files = input.files;

                    if (!files.length) {
                        alert("업로드할 파일이 없습니다.");
                        return;
                    }

                    const formData = new FormData();
                    for (let i = 0; i < files.length; i++) {
                        formData.append("files", files[i]);
                    }

                    const res = await fetch("/upload", {
                        method: "POST",
                        body: formData
                    });

                    const result = await res.json();
                    const messages = [];

                    for (const fileObj of result.files) {
                        const filename = Object.keys(fileObj)[0];
                        const data = fileObj[filename];

                        let message = `✅ ${filename} 업로드 성공`;

                        if (data.body) {
                            try {
                                const parsedBody = JSON.parse(data.body);
                                if (parsedBody.error) {
                                    message = `❌ ${filename}: ${parsedBody.error}`;
                                }
                            } catch (e) {
                                // body 파싱 실패 시 무시
                            }
                        }

                        if (data.status_code >= 400) {
                            message = `❌ ${filename}: 업로드 실패`;
                        }

                        messages.push(message);
                    }

                    // ✅ 결과 메시지 출력
                    document.getElementById("upload-result").innerText = messages.join("\n");
                }
            </script>


        </body>
    </html>
    """