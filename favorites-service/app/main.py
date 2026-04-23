from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routes.favorite_routes import router

# ── Création automatique des tables ──────────────────────────
Base.metadata.create_all(bind=engine)

# ── Initialisation de l'application FastAPI ─────────────────
app = FastAPI(
    title="Favorites Service",
    description="Microservice de gestion des séries favorites",
    version="1.0.0",
    docs_url="/favorites/docs",
    openapi_url="/favorites/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Inclusion des routes ─────────────────────────────────────
app.include_router(router)