"""Поиск по сегментам и ответ с таймингами."""

from __future__ import annotations

import re

from pydantic import BaseModel

from app.services.videos import all_videos

_WORD_RE = re.compile(r"[a-zA-Z]+")

STOPWORDS = {
    "how", "what", "when", "where", "why", "which", "who", "to", "the", "a", "an",
    "and", "or", "of", "in", "on", "for", "is", "are", "be", "do", "does",
}


class Hit(BaseModel):
    video: str
    video_id: str
    stamp: str
    seconds: int
    text: str
    score: float


class TubeAnswer(BaseModel):
    question: str
    answer: str
    segments: list[Hit]


def stamp(seconds: int) -> str:
    """Секунды в mm:ss. Детерминировано."""
    if seconds < 0:
        raise ValueError("seconds must be >= 0")
    return f"{seconds // 60:02d}:{seconds % 60:02d}"


def search_segments(question: str, top_k: int = 3, min_score: float = 1.0) -> list[Hit]:
    """Найти сегменты по пересечению слов."""
    if not question or not question.strip():
        raise ValueError("question must not be empty")
    terms = set(_WORD_RE.findall(question.lower())) - STOPWORDS
    hits: list[Hit] = []
    for video in all_videos():
        for segment in video.segments:
            overlap = len(terms & set(_WORD_RE.findall(segment.text.lower())))
            if overlap >= min_score:
                hits.append(
                    Hit(
                        video=video.title,
                        video_id=video.id,
                        stamp=stamp(segment.t),
                        seconds=segment.t,
                        text=segment.text,
                        score=float(overlap),
                    )
                )
    hits.sort(key=lambda hit: (-hit.score, hit.video, hit.seconds))
    return hits[: max(top_k, 0)]


def ask(question: str, top_k: int = 3, min_score: float = 1.0) -> TubeAnswer:
    """Ответить с таймингами сегментов."""
    hits = search_segments(question, top_k, min_score)
    if not hits:
        return TubeAnswer(question=question.strip(), answer="Nothing found in transcripts.", segments=[])
    parts = [f"{hit.text.rstrip('.')} [{hit.stamp}]" for hit in hits]
    return TubeAnswer(question=question.strip(), answer=" ".join(parts) + ".", segments=hits)
