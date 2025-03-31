from fastapi import FastAPI

# 
app = FastAPI(root_path="/api")

@app.get("/")
def read_root():
    return {"message": "🚀 FastAPI with root_path '/api'"}