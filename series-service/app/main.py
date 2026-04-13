from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.series_routes import router as series_router

app = FastAPI(
    title="Series Service",
    version="1.1.0"
)

# CORS doit être ajouté AVANT include_router
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(series_router)

@app.get("/")
def home():
    return {"service": "series-service", "status": "running"}

@app.get("/health")
def health():
    return {"status": "UP"}