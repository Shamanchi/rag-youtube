"""Эндпоинты видео и вопросов."""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from app.core.config import Settings, get_settings
from app.services.search import TubeAnswer, ask
from app.services.videos import Video, all_videos, find_video

router = APIRouter()


class AskRequest(BaseModel):
    question: str = Field(min_length=1, max_length=500)


@router.get("/videos", response_model=list[Video])
async def videos(q: str = "") -> list[Video]:
    query = q.strip().lower()
    if not query:
        return all_videos()
    return [video for video in all_videos() if query in f"{video.title}".lower()]


@router.get("/videos/{video_id}", response_model=Video)
async def video(video_id: str) -> Video:
    found = find_video(video_id)
    if found is None:
        raise HTTPException(status_code=404, detail=f"video {video_id} not found")
    return found


@router.post("/ask", response_model=TubeAnswer)
async def ask_endpoint(
    request: AskRequest,
    settings: Settings = Depends(get_settings),
) -> TubeAnswer:
    try:
        return ask(request.question, settings.top_k, settings.min_score)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
