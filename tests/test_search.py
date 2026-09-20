"""Unit-тесты поиска: без сети, детерминированы."""

import pytest

from app.services.search import ask, search_segments, stamp
from app.services.videos import all_videos, find_video


def test_stamp() -> None:
    assert stamp(0) == "00:00"
    assert stamp(65) == "01:05"
    assert stamp(130) == "02:10"
    with pytest.raises(ValueError):
        stamp(-1)


def test_search_index_question() -> None:
    hits = search_segments("How to build the index?")
    assert len(hits) == 1
    assert hits[0].video_id == "v1"
    assert hits[0].stamp == "00:00"


def test_search_compose() -> None:
    hits = search_segments("compose up builds the stack")
    assert len(hits) == 1
    assert hits[0].video_id == "v2"
    assert hits[0].seconds == 45


def test_ask_answer() -> None:
    result = ask("How to build the index?")
    assert "[00:00]" in result.answer
    assert result.segments[0].video == "Vector DB crash course"


def test_no_match() -> None:
    result = ask("quantum knitting patterns")
    assert result.segments == []
    assert "Nothing found" in result.answer
    with pytest.raises(ValueError):
        search_segments("   ")


def test_videos() -> None:
    assert len(all_videos()) == 2
    assert find_video("v1") is not None
    assert find_video("ghost") is None
