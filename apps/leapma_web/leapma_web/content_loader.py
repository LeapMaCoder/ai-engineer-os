"""Load LeapMa-original Python track content (not competitor copies)."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

_CONTENT = Path(__file__).resolve().parents[1] / "content" / "python"

_EXERCISE_KEYS = (
    "type",
    "prompt",
    "hint",
    "options",
    "answers",
    "checks",
    "pass_feedback",
    "fail_prefix",
)


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
    raw = json.loads(_chapter_path(chapter_id).read_text(encoding="utf-8-sig"))
    lessons = raw.get("lessons") or []
    raw["lessons"] = [normalize_lesson(x) for x in lessons]
    return raw


def _normalize_story(story_raw: Any, lesson_title: str) -> dict[str, str] | None:
    """Normalize ``concept.story``: legacy string → object; fill missing fields.

    Ready shape::
        {mission_title, scene, npc, npc_line, objective, body, clear_hint?}
    """
    if story_raw is None:
        return None
    if isinstance(story_raw, str):
        body = story_raw.strip()
        if not body:
            return None
        raw: dict[str, Any] = {"body": body}
    elif isinstance(story_raw, dict):
        keys = (
            "mission_title",
            "scene",
            "npc",
            "npc_line",
            "objective",
            "body",
            "clear_hint",
        )
        if not any(str(story_raw.get(k) or "").strip() for k in keys):
            return None
        raw = story_raw
    else:
        return None

    title = (lesson_title or "").strip() or "任务简报"

    def pick(key: str, default: str) -> str:
        val = raw.get(key)
        if val is None:
            return default
        text = str(val).strip()
        return text if text else default

    return {
        "mission_title": pick("mission_title", title),
        "scene": pick("scene", "训练终端"),
        "npc": pick("npc", "跃"),
        "npc_line": pick("npc_line", "先说你以为发生了什么。"),
        "objective": pick("objective", "完成本关练习并通过判定。"),
        "body": pick("body", ""),
        "clear_hint": pick("clear_hint", ""),
    }


def normalize_lesson(raw: dict[str, Any]) -> dict[str, Any]:
    """Normalize concept / example / exercises into a stable lesson shape.

    Compatible with:
    - flat exercise fields (type/prompt/…) on the lesson (legacy)
    - nested ``exercises[]`` (first item promoted when flat fields missing)
    - ``concept`` as str or ``{normal, story?}``
    - ``story`` as str (→ ``{body}`` + defaults) or mission object
    - ``example`` as str or ``{code, note?}``
    """
    lesson = dict(raw)

    exercises = lesson.get("exercises")
    if isinstance(exercises, list) and exercises:
        ex0 = exercises[0] if isinstance(exercises[0], dict) else {}
        for key in _EXERCISE_KEYS:
            cur = lesson.get(key)
            empty = cur is None or cur == "" or cur == []
            if empty and key in ex0:
                lesson[key] = ex0[key]

    title = (lesson.get("title") or "").strip()
    concept = lesson.get("concept")
    if isinstance(concept, str):
        lesson["concept"] = {"normal": concept.strip(), "story": None}
    elif isinstance(concept, dict):
        normal = (concept.get("normal") or "").strip()
        story = _normalize_story(concept.get("story"), title)
        lesson["concept"] = {"normal": normal, "story": story}
    else:
        # Legacy: coach as thin concept fallback (UI still shows 【学】)
        fallback = (lesson.get("coach") or "").strip()
        lesson["concept"] = {"normal": fallback, "story": None}

    example = lesson.get("example")
    if isinstance(example, str):
        lesson["example"] = {"code": example, "note": ""}
    elif isinstance(example, dict):
        lesson["example"] = {
            "code": example.get("code") or example.get("text") or "",
            "note": example.get("note") or "",
        }
    else:
        lesson["example"] = {"code": "", "note": ""}

    lesson["has_story"] = bool(lesson["concept"].get("story"))
    return lesson


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


def prev_lesson(chapter_id: str, lesson_id: str) -> tuple[str, str] | None:
    lessons = load_chapter(chapter_id).get("lessons") or []
    ids = [x["id"] for x in lessons]
    if lesson_id not in ids:
        return None
    i = ids.index(lesson_id)
    if i > 0:
        return chapter_id, ids[i - 1]
    chapters = list_chapters()
    cids = [c["id"] for c in chapters]
    if chapter_id not in cids:
        return None
    ci = cids.index(chapter_id)
    if ci <= 0:
        return None
    prev_ch = cids[ci - 1]
    prev_lessons = load_chapter(prev_ch).get("lessons") or []
    if not prev_lessons:
        return None
    return prev_ch, prev_lessons[-1]["id"]


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
