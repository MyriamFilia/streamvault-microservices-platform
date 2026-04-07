from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"status": "Service Séries TV opérationnel", "python_version": "3.14.3"}

@app.get("/health")
def health():
    return {"status": "UP"}