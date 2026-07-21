"""Orientation helpers — coach-first, not survey (方案 1)."""

from __future__ import annotations

import re

# Extreme vagueness: short / generic "学编程" style — probe may be *suggested*, never required.
_VAGUE_ONLY = re.compile(
    r"^\s*(我想|我要|想要|希望)?"
    r"(学|学习|提升|提高|补强|加强)?"
    r"(一下|点|些)?"
    r"(编程|写代码|代码|技术|计算机|软件|IT|开发)?"
    r"(能力|水平|技能)?"
    r"[!！。.\s]*$",
    re.I,
)

_CONCRETE = re.compile(
    r"python|java|javascript|typescript|golang|\bgo\b|rust|c\+\+|前端|后端|全栈|"
    r"算法|数据结构|数据库|mysql|redis|linux|docker|react|vue|节点|"
    r"脚本|接口|api|微服务|面试|职场|转岗|spring|django|flask|"
    r"机器学习|深度学习|ai\b|爬虫|运维|测试|安全",
    re.I,
)


def is_extremely_vague_goal(goal: str) -> bool:
    """True only when goal is extremely vague (方案 1: probe default skip)."""
    g = (goal or "").strip()
    if len(g) < 6:
        return True
    if _CONCRETE.search(g):
        return False
    if _VAGUE_ONLY.match(g):
        return True
    # No concrete signal and still short → treat as extremely vague
    return len(g) < 14
