from fastapi import FastAPI

from app.core.config import get_settings
from app.core.models import VideoJob, VideoRequest
from app.services.pipeline import VideoPlanningPipeline

settings = get_settings()
app = FastAPI(title=settings.app_name, version="0.1.0")
pipeline = VideoPlanningPipeline()


@app.get("/")
def root() -> dict[str, str]:
    return {
        "name": settings.app_name,
        "status": "running",
        "docs": "/docs",
    }


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "healthy",
        "environment": settings.app_env,
        "llm_provider": settings.llm_provider,
    }


@app.post("/api/v1/video-jobs/plan", response_model=VideoJob)
def plan_video(request: VideoRequest) -> VideoJob:
    return pipeline.run(request)
