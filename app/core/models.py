from enum import StrEnum
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Platform(StrEnum):
    youtube_shorts = "youtube_shorts"
    tiktok = "tiktok"
    instagram_reels = "instagram_reels"


class VideoRequest(BaseModel):
    topic: str = Field(min_length=3, max_length=300)
    audience: str = Field(default="general audience", max_length=200)
    platform: Platform = Platform.youtube_shorts
    duration_seconds: int = Field(default=60, ge=15, le=180)
    tone: str = Field(default="engaging", max_length=100)


class Source(BaseModel):
    title: str
    url: str | None = None
    summary: str


class ResearchResult(BaseModel):
    topic: str
    angle: str
    key_points: list[str]
    sources: list[Source] = Field(default_factory=list)


class Script(BaseModel):
    hook: str
    narration: str
    call_to_action: str
    estimated_duration_seconds: int


class Scene(BaseModel):
    number: int
    duration_seconds: int
    narration: str
    visual_prompt: str
    on_screen_text: str | None = None


class VideoJob(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    request: VideoRequest
    research: ResearchResult
    script: Script
    scenes: list[Scene]
    status: str = "planned"
