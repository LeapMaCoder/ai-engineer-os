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
            body="本章练习尚未开放（骨架占位）。请先完成第 1～3 章 ready 练习。",
        )
    if not text:
        return GradeResult(passed=False, body="先写一小段再提交——我们马上判定。")

    # Hard No: whole-project codegen as main ask
    if re.search(r"(整(个)?项目|帮我写完|代写.*项目|直接生成.*(项目|全部代码))", text, re.I):
        return GradeResult(
            passed=False,
            body=(
                "这更像「代写整个项目」请求，不是本练习主价值（Hard No）。\n"
                "请只提交本课要求的一小段可判定作答。"
            ),
        )

    qtype = (lesson.get("type") or "code").lower()
    if qtype == "mcq":
        return _grade_mcq(lesson, text)
    if qtype == "fill":
        return _grade_fill(lesson, text)
    if qtype == "short":
        return _grade_with_checks(lesson, text)
    # code (default) and any unknown → checks
    return _grade_with_checks(lesson, text)


def _fail(lesson: dict[str, Any], failures: list[str]) -> GradeResult:
    prefix = lesson.get("fail_prefix") or "还差一点："
    body = prefix + "\n- " + "\n- ".join(failures)
    hint = lesson.get("hint") or ""
    if hint:
        body += f"\n提示：{hint}"
    return GradeResult(passed=False, body=body)


def _pass(lesson: dict[str, Any]) -> GradeResult:
    return GradeResult(
        passed=True,
        body=lesson.get("pass_feedback") or "通过。继续下一练。",
    )


def _norm_compact(s: str) -> str:
    return re.sub(r"\s+", "", (s or "").strip().lower())


def _grade_mcq(lesson: dict[str, Any], text: str) -> GradeResult:
    expected = [str(a).strip().upper() for a in (lesson.get("answers") or [])]
    got = text.strip().upper()
    # Accept "B" or "B. ..." or option id only
    if re.match(r"^[A-D]\b", got):
        got = got[0]
    if got in expected:
        return _pass(lesson)
    # Also allow matching option text if user pasted full line
    for opt in lesson.get("options") or []:
        oid = str(opt.get("id", "")).strip().upper()
        if oid in expected and _norm_compact(opt.get("text", "")) == _norm_compact(text):
            return _pass(lesson)
    return _fail(lesson, ["选项不正确，再读一遍题干与选项。"])


def _grade_fill(lesson: dict[str, Any], text: str) -> GradeResult:
    answers = lesson.get("answers") or []
    compact = _norm_compact(text)
    for ans in answers:
        a = _norm_compact(str(ans))
        if not a:
            continue
        if compact == a or a in compact or compact in a:
            return _pass(lesson)
    # Fall through to checks if provided
    checks = lesson.get("checks") or []
    if checks:
        return _grade_with_checks(lesson, text)
    return _fail(lesson, ["填空内容与期望不符，看看类型与运算是否匹配。"])


def _grade_with_checks(lesson: dict[str, Any], text: str) -> GradeResult:
    failures: list[str] = []
    for check in lesson.get("checks") or []:
        ok, msg = _run_check(check, text)
        if not ok:
            failures.append(msg or "未通过检查")
    if failures:
        return _fail(lesson, failures)
    return _pass(lesson)


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
    if t == "keywords_any":
        vals = check.get("values") or []
        low = text.lower()
        ok = any(str(v).lower() in low for v in vals)
        return (ok, str(check.get("message") or "未覆盖关键要点"))
    if t == "keywords_all_groups":
        groups = check.get("groups") or []
        low = text.lower()
        ok = all(
            any(str(k).lower() in low for k in (g or [])) for g in groups
        )
        return (ok, str(check.get("message") or "要点不完整"))
    return True, ""
