"""Quick content checks for Python ch01–03 ready lessons."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent / "content" / "python"
CHAPTERS = ["chapter_01.json", "chapter_02.json", "chapter_03.json"]
NPCS_PATH = ROOT / "npcs.json"

_STORY_REQUIRED = (
    "mission_title",
    "scene",
    "npc",
    "npc_line",
    "objective",
    "body",
)


def _allowed_npc_names() -> set[str]:
    data = json.loads(NPCS_PATH.read_text(encoding="utf-8"))
    return {str(n.get("display_name") or "").strip() for n in (data.get("npcs") or [])}


def main() -> int:
    errors: list[str] = []
    if not NPCS_PATH.is_file():
        print(f"FAIL: missing {NPCS_PATH}")
        return 1
    allowed = _allowed_npc_names()
    if len(allowed) != 4:
        errors.append(f"npcs.json must list exactly 4 display_name, got {sorted(allowed)}")

    for name in CHAPTERS:
        data = json.loads((ROOT / name).read_text(encoding="utf-8"))
        for lesson in data.get("lessons") or []:
            lid = lesson.get("id", "?")
            concept = lesson.get("concept") or {}
            story = concept.get("story")
            if not isinstance(story, dict):
                errors.append(f"{lid}: concept.story must be an object (got {type(story).__name__})")
            else:
                for key in _STORY_REQUIRED:
                    if not str(story.get(key) or "").strip():
                        errors.append(f"{lid}: missing concept.story.{key}")
                npc = str(story.get("npc") or "").strip()
                if npc and npc not in allowed:
                    errors.append(
                        f"{lid}: story.npc {npc!r} not in npcs.json display_name {sorted(allowed)}"
                    )
            example = lesson.get("example") or {}
            code = (example.get("code") or "").strip()
            note = (example.get("note") or "").strip()
            if not code:
                errors.append(f"{lid}: missing example.code")
            if not note:
                errors.append(f"{lid}: missing example.note")
            prompt = (lesson.get("prompt") or "").strip()
            if code and prompt and code == prompt:
                errors.append(f"{lid}: example.code identical to prompt")
            code_norm = "".join(code.split())
            prompt_norm = "".join(prompt.split())
            if code_norm and prompt_norm and code_norm == prompt_norm:
                errors.append(f"{lid}: example.code matches prompt (whitespace-insensitive)")
            if code and prompt and code in prompt and len(code) > 20:
                errors.append(f"{lid}: example.code embedded verbatim in prompt")

    if errors:
        print("FAIL:")
        for e in errors:
            print(" -", e)
        return 1
    print(
        f"OK: {len(CHAPTERS)} chapters; story NPCs ∈ {sorted(allowed)}; "
        "story-mission + example; example≠prompt."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
