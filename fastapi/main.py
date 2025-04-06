# ✅ 수정된 FastAPI 코드
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

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
