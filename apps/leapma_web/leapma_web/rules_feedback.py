"""Deterministic rule-based exercise feedback (LLM optional / Later)."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any


@dataclass
class GradeResult:
    passed: bool
    body: str
    uncertain: bool = False


def grade_lesson(lesson: dict[str, Any], attempt: str) -> GradeResult:
    text = (attempt or "").strip()
    if lesson.get("locked"):
        return GradeResult(
            passed=False,
            body="本章练习尚未开放（骨架占位）。请先完成第 1 章 ready 练习。",
        )
    if not text:
        return GradeResult(passed=False, body="先写一小段再提交——我们马上判定。")

    # Hard No: whole-project codegen as main ask
    if re.search(r"(整(个)?项目|帮我写完|代写.*项目|直接生成.*(项目|全部代码))", text, re.I):
        return GradeResult(
            passed=False,
            body=(
                "这更像「代写整个项目」请求，不是本练习主价值（Hard No）。\n"
                "请只提交本课要求的一小段可判定代码。"
            ),
        )

    failures: list[str] = []
    for check in lesson.get("checks") or []:
        ok, msg = _run_check(check, text)
        if not ok:
            failures.append(msg or "未通过检查")

    if failures:
        prefix = lesson.get("fail_prefix") or "还差一点："
        body = prefix + "\n- " + "\n- ".join(failures)
        hint = lesson.get("hint") or ""
        if hint:
            body += f"\n提示：{hint}"
        return GradeResult(passed=False, body=body)

    return GradeResult(
        passed=True,
        body=lesson.get("pass_feedback") or "通过。继续下一练。",
    )


def _run_check(check: dict[str, Any], text: str) -> tuple[bool, str]:
    t = check.get("type")
    if t == "contains":
        val = str(check.get("value", ""))
        return (val in text, str(check.get("message") or f"需包含 {val}"))
    if t == "contains_any":
        vals = check.get("values") or []
        ok = any(str(v) in text for v in vals)
        return (ok, str(check.get("message") or "未包含期望内容"))
    if t == "regex":
        pat = str(check.get("pattern", ""))
        ok = re.search(pat, text, re.I | re.M) is not None
        return (ok, str(check.get("message") or "格式不符合"))
    if t == "min_print_calls":
        n = int(check.get("value") or 0)
        count = len(re.findall(r"print\s*\(", text, re.I))
        return (count >= n, str(check.get("message") or f"至少需要 {n} 个 print"))
    return True, ""
