from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Voice Clone 서비스에 오신 것을 환영합니다!"}
