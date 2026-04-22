from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routes.user_routes import router as user_router

# Crée les tables automatiquement au démarrage
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="User Service",
    description="Gestion des utilisateurs et authentification JWT",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)


@app.get("/")
def home():
    return {"service": "User Service", "status": "running"}


@app.get("/health")
def health():
    return {"status": "UP"}