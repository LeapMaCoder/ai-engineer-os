"""Load LeapMa-original Python track content (not competitor copies)."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

_CONTENT = Path(__file__).resolve().parents[1] / "content" / "python"


def _chapter_path(chapter_id: str) -> Path:
    """Map py-01 → chapter_01.json, py-15 → chapter_15.json."""
    try:
        num = int(str(chapter_id).split("-", 1)[1])
    except (IndexError, ValueError) as exc:
        raise KeyError(chapter_id) from exc
    path = _CONTENT / f"chapter_{num:02d}.json"
    if not path.is_file():
        raise KeyError(chapter_id)
    return path


@lru_cache(maxsize=1)
def load_track() -> dict[str, Any]:
    return json.loads((_CONTENT / "track.json").read_text(encoding="utf-8-sig"))


@lru_cache(maxsize=32)
def load_chapter(chapter_id: str) -> dict[str, Any]:
    return json.loads(_chapter_path(chapter_id).read_text(encoding="utf-8-sig"))


def list_chapters() -> list[dict[str, Any]]:
    return list(load_track()["chapters"])


def get_lesson(chapter_id: str, lesson_id: str) -> dict[str, Any] | None:
    ch = load_chapter(chapter_id)
    for lesson in ch.get("lessons", []):
        if lesson["id"] == lesson_id:
            return lesson
    return None


def first_lesson_id(chapter_id: str) -> str | None:
    lessons = load_chapter(chapter_id).get("lessons") or []
    return lessons[0]["id"] if lessons else None


def chapter_is_playable(chapter_id: str) -> bool:
    meta = next((c for c in list_chapters() if c["id"] == chapter_id), None)
    if not meta or meta.get("status") != "ready":
        return False
    ch = load_chapter(chapter_id)
    return any(not x.get("locked") for x in (ch.get("lessons") or []))


def next_lesson(chapter_id: str, lesson_id: str) -> tuple[str, str] | None:
    lessons = load_chapter(chapter_id).get("lessons") or []
    ids = [x["id"] for x in lessons]
    if lesson_id not in ids:
        return None
    i = ids.index(lesson_id)
    if i + 1 < len(ids):
        return chapter_id, ids[i + 1]
    chapters = list_chapters()
    cids = [c["id"] for c in chapters]
    if chapter_id not in cids:
        return None
    ci = cids.index(chapter_id)
    if ci + 1 < len(cids):
        nid = first_lesson_id(cids[ci + 1])
        if nid:
            return cids[ci + 1], nid
    return None
