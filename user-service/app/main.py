from fastapi import FastAPI
from app.database import engine, Base
from app.routes.user_routes import router as user_router

# Crée les tables automatiquement au démarrage
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="User Service",
    description="Gestion des utilisateurs et authentification JWT",
    version="1.0.0"
)

app.include_router(user_router)


@app.get("/")
def home():
    return {"status": "User Service opérationnel", "version": "1.0.0"}


@app.get("/health")
def health():
    return {"status": "UP"}