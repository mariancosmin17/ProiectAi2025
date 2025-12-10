from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.nash.api import router as nash_router
from app.csp.api import router as csp_router

app = FastAPI(title="SmarTest (simplu)")

# CORS (în dev poți lăsa * sau specifică localhost:5173 pentru React)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["health"])
def health():
    return {"message": "Serverul este activ."}

# API v1
app.include_router(nash_router, prefix="/api/v1")
app.include_router(csp_router, prefix="/api/v1")