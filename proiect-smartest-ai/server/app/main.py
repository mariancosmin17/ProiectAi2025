# server/app/main.py

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app. nash.api import router as nash_router
from app.csp. api import router as csp_router
from app.search.api import router as search_router
from app.path.api import router as path_router
from app.graph.api import router as graph_router

# 👇 Comentat până când implementăm modulul alphabeta
from app. alphabeta.api import router as alphabeta_router

app = FastAPI(
    title="SmarTest AI Question Generator",
    version="1.0.0",
    description="Generare și evaluare întrebări pentru examenul de Inteligență Artificială"
)

# ---------------------- CORS (dev) ----------------------
DEFAULT_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
ENV_ORIGIN = os.getenv("FRONTEND_URL")
ALLOW_ORIGINS = [ENV_ORIGIN] if ENV_ORIGIN else DEFAULT_ORIGINS + ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------- Health ----------------------
@app.get("/", tags=["health"])
def root():
    return {
        "message": "SmarTest API este activ",
        "version": "1.0.0",
        "modules": ["Nash Equilibrium", "CSP Solver", "Search Strategies", "Alpha-Beta Pruning", "Pathfinding", "Graph"]
    }

# ---------------------- API v1 ----------------------
app.include_router(nash_router, prefix="/api/v1")
app.include_router(csp_router, prefix="/api/v1")
app.include_router(search_router, prefix="/api/v1")
app.include_router(alphabeta_router, prefix="/api/v1")
app.include_router(path_router, prefix="/api/v1")
app.include_router(graph_router, prefix="/api/v1")
