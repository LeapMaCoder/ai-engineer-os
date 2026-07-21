"""Load LeapMa-original Python track content (not competitor copies)."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

_CONTENT = Path(__file__).resolve().parents[1] / "content" / "python"


@lru_cache(maxsize=1)
def load_track() -> dict[str, Any]:
    return json.loads((_CONTENT / "track.json").read_text(encoding="utf-8"))


@lru_cache(maxsize=8)
def load_chapter(chapter_id: str) -> dict[str, Any]:
    mapping = {
        "py-01": "chapter_01.json",
        "py-02": "chapter_02.json",
        "py-03": "chapter_03.json",
    }
    name = mapping.get(chapter_id)
    if not name:
        raise KeyError(chapter_id)
    return json.loads((_CONTENT / name).read_text(encoding="utf-8"))


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


def next_lesson(chapter_id: str, lesson_id: str) -> tuple[str, str] | None:
    lessons = load_chapter(chapter_id).get("lessons") or []
    ids = [x["id"] for x in lessons]
    if lesson_id not in ids:
        return None
    i = ids.index(lesson_id)
    if i + 1 < len(ids):
        return chapter_id, ids[i + 1]
    # next chapter first lesson if any
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
