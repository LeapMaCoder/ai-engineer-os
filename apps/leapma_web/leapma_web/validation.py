"""App-side validation of LLM / progress outputs (Spec AI Behavior)."""

from __future__ import annotations

import re

from leapma_web.llm import FeedbackResult

_EMPTY_PRAISE = re.compile(r"^(你很棒|加油|太强了|继续保持)[！!。.\s]*$", re.I)
_FAKE_LEVEL = re.compile(r"(等级\s*\+?\d+|升到\s*LV|暴涨|段位飞升)", re.I)


def validate_feedback(result: FeedbackResult) -> FeedbackResult:
    body = (result.body or "").strip()
    if not body:
        return FeedbackResult(
            body="坦诚边界：系统未产生可用反馈。请缩小问题后重试。",
            uncertain=True,
            rejected_codegen=result.rejected_codegen,
        )
    if _EMPTY_PRAISE.match(body) and not result.uncertain:
        return FeedbackResult(
            body=(
                "反馈被拦截：纯情绪夸奖不足以通过验收（AC-02a）。\n"
                "请描述具体对错或改进点；若无法判断请走不确定分支。"
            ),
            uncertain=True,
            rejected_codegen=result.rejected_codegen,
        )
    return FeedbackResult(
        body=body,
        uncertain=result.uncertain,
        rejected_codegen=result.rejected_codegen,
    )


def validate_progress_note(note: str) -> tuple[bool, str]:
    text = (note or "").strip()
    if len(text) < 8:
        return False, "请写出相对目标的至少一点具体进展（不要只写空夸奖）。"
    if _EMPTY_PRAISE.match(text) or _FAKE_LEVEL.search(text):
        return False, "禁止用空夸奖或假等级代替相对目标的具体进展（OQ-003）。"
    return True, text
