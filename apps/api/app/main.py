from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .database import Base, engine
from .routes.evals import router as evals_router
from .routes.health import router as health_router
from .routes.intake import router as intake_router
from .routes.lab import router as lab_router
from .routes.metrics import router as metrics_router
from .routes.demo import router as demo_router
from .routes.novelty import router as novelty_router
from .routes.tickets import router as tickets_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name, version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, prefix=settings.api_prefix)
app.include_router(intake_router, prefix=settings.api_prefix)
app.include_router(tickets_router, prefix=settings.api_prefix)
app.include_router(metrics_router, prefix=settings.api_prefix)
app.include_router(evals_router, prefix=settings.api_prefix)
app.include_router(novelty_router, prefix=settings.api_prefix)
app.include_router(lab_router, prefix=settings.api_prefix)
app.include_router(demo_router, prefix=settings.api_prefix)
