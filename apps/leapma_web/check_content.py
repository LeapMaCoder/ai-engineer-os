"""Quick content checks for Python ch01–03 ready lessons."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent / "content" / "python"
CHAPTERS = ["chapter_01.json", "chapter_02.json", "chapter_03.json"]

_STORY_REQUIRED = (
    "mission_title",
    "scene",
    "npc",
    "npc_line",
    "objective",
    "body",
)


def main() -> int:
    errors: list[str] = []
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
            # Normalize whitespace for soft equality vs prompt code fences
            code_norm = "".join(code.split())
            prompt_norm = "".join(prompt.split())
            if code_norm and prompt_norm and code_norm == prompt_norm:
                errors.append(f"{lid}: example.code matches prompt (whitespace-insensitive)")
            # Also reject if example code block appears verbatim inside prompt
            if code and prompt and code in prompt and len(code) > 20:
                errors.append(f"{lid}: example.code embedded verbatim in prompt")

    if errors:
        print("FAIL:")
        for e in errors:
            print(" -", e)
        return 1
    print(
        f"OK: {len(CHAPTERS)} chapters, all ready lessons have "
        "story-mission object + example; example≠prompt."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
