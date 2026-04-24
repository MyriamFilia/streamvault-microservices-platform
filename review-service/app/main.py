from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routes.review_routes import router

# Création automatique des tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Review Service",
    description="Microservice de gestion des reviews",
    version="1.0.0",
    docs_url="/reviews/docs",
    openapi_url="/reviews/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router)