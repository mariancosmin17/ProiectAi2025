# server/app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.nash import api as nash_api
import os

app = FastAPI(
    title="SmarTest (simplu)",
    version="1.0.0",
)

# ---------------------- CORS (dev) ----------------------
# Poți seta FRONTEND_URL în env, altfel permite localhost și *
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
    return {"message": "Serverul este activ."}

@app.get("/health", tags=["health"])
def health():
    return {"status": "ok"}

@app.get("/ready", tags=["health"])
def ready():
    return {"ready": True}

# ---------------------- API v1 ----------------------
# IMPORTANT: routerul pentru Nash este montat pe /api/v1
app.include_router(nash_api.router, prefix="/api/v1")

# ---------------------- Run local ----------------------
# Permite rularea directă: `python main.py`
if __name__ == "__main__":
    import uvicorn
    # Pornește pe 0.0.0.0:8000, reîncărcare activă în dev
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
