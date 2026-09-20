"""Mock-видео с транскриптами по сегментам. Без сети."""

from __future__ import annotations

from pydantic import BaseModel


class Segment(BaseModel):
    t: int
    text: str


class Video(BaseModel):
    id: str
    title: str
    segments: list[Segment]


_VIDEOS: list[Video] = [
    Video(
        id="v1",
        title="Vector DB crash course",
        segments=[
            Segment(t=0, text="Welcome, today we index vectors for search."),
            Segment(t=65, text="IVFFlat suits medium collections with clear clusters."),
            Segment(t=130, text="Use HNSW for large collections and fast recall."),
        ],
    ),
    Video(
        id="v2",
        title="Docker in 100 seconds",
        segments=[
            Segment(t=0, text="Images, containers and volumes explained quickly."),
            Segment(t=45, text="Compose up builds and starts the whole stack."),
        ],
    ),
]


def all_videos() -> list[Video]:
    return list(_VIDEOS)


def find_video(video_id: str) -> Video | None:
    for video in _VIDEOS:
        if video.id == video_id:
            return video
    return None
