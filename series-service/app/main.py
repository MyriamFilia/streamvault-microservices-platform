from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.series_routes import router as series_router
import threading
from contextlib import asynccontextmanager
from app.grpc_server import serve

@asynccontextmanager
async def lifespan(app: FastAPI):
    thread = threading.Thread(target=serve, daemon=True)
    thread.start()
    print("gRPC server started on port 50051")
    yield
    print("Shutting down...")

app = FastAPI(
    title="Series Service",
    version="1.1.0",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
    lifespan=lifespan
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
