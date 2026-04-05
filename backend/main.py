import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, FileResponse
from contextlib import asynccontextmanager
from config import settings
from db.session_store import init_db
from api.chat import router as chat_router
from api.sessions import router as sessions_router
from api.models import router as models_router
from api.repo import router as repo_router
from tools.registry import get_tools

FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "frontend_dist")

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(title="Claw-Code Agent", version="1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API routes first
app.include_router(chat_router, prefix="/api")
app.include_router(sessions_router, prefix="/api")
app.include_router(models_router, prefix="/api")
app.include_router(repo_router, prefix="/api")

# Serve static frontend from /frontend_dist
if os.path.exists(FRONTEND_DIR):
    app.mount("/assets", StaticFiles(directory=os.path.join(FRONTEND_DIR, "assets")), name="assets")

@app.get("/api/tools")
async def list_tools():
    return {"tools": get_tools()}

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/")
async def serve_index():
    index_path = os.path.join(FRONTEND_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Claw-Code Agent API - frontend not built"}