from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import alerts, caregivers, patients, vitals
from db.supabase_client import get_settings


settings = get_settings()


app = FastAPI(
    title="CareOrchestrator API",
    description="Multi-agent AI system for proactive chronic disease management",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        origin.strip()
        for origin in settings.frontend_origin.split(",")
        if origin.strip()
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(patients.router)
app.include_router(vitals.router)
app.include_router(alerts.router)
app.include_router(caregivers.router)


@app.get("/")
def root():
    return {
        "service": "CareOrchestrator API",
        "status": "running",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "orchestrator_enabled": settings.orchestrator_enabled,
        "orchestrator_interval_hours": settings.orchestrator_interval_hours,
    }