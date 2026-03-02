from fastapi import FastAPI

from app.api.v1 import auth, billing, plans, resume_analysis
from app.core.config import settings
from app.db.base import create_tables

app = FastAPI(title=settings.app_name)


@app.on_event("startup")
def startup() -> None:
    create_tables()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "app": settings.app_name}


app.include_router(auth.router, prefix="/api/v1")
app.include_router(plans.router, prefix="/api/v1")
app.include_router(billing.router, prefix="/api/v1")
app.include_router(resume_analysis.router, prefix="/api/v1")
