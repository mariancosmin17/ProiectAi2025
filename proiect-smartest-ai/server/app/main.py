# server/app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.nash.api import router as nash_router
from app.csp.api import router as csp_router

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

# API v1
app.include_router(nash_router, prefix="/api/v1")
app.include_router(csp_router, prefix="/api/v1")