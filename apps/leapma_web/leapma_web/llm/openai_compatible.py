"""Optional OpenAI-compatible adapter — not locked to one vendor (AQ-002).

Set:
  LEAPMA_LLM_PROVIDER=openai_compatible
  LEAPMA_LLM_BASE_URL=https://api.openai.com/v1   # or any compatible endpoint
  LEAPMA_LLM_API_KEY=...
  LEAPMA_LLM_MODEL=gpt-4o-mini
"""

from __future__ import annotations

import json
import os
import re

import httpx

from leapma_web.llm import FeedbackResult, LLMProvider, OrientationAssist
from leapma_web.llm.mock import MockProvider, _CODEGEN_RE

_fallback = MockProvider()


class OpenAICompatibleProvider(LLMProvider):
    def __init__(self) -> None:
        self.base_url = os.getenv("LEAPMA_LLM_BASE_URL", "https://api.openai.com/v1").rstrip(
            "/"
        )
        self.api_key = os.getenv("LEAPMA_LLM_API_KEY", "")
        self.model = os.getenv("LEAPMA_LLM_MODEL", "gpt-4o-mini")

    def _chat(self, system: str, user: str) -> str:
        if not self.api_key:
            raise RuntimeError("LEAPMA_LLM_API_KEY missing; use mock provider or set key")
        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "temperature": 0.3,
        }
        with httpx.Client(timeout=60.0) as client:
            r = client.post(url, headers=headers, json=payload)
            r.raise_for_status()
            data = r.json()
        return data["choices"][0]["message"]["content"]

    def assist_orientation(self, goal_intent: str) -> OrientationAssist:
        try:
            raw = self._chat(
                "You help programmers set a tiny next practice step. "
                "Reply JSON keys: position_hint, probe_question, next_step, exercise_prompt. "
                "Chinese. No course catalog. No whole-project codegen.",
                f"goal_intent: {goal_intent}",
            )
            m = re.search(r"\{.*\}", raw, re.S)
            obj = json.loads(m.group(0) if m else raw)
            return OrientationAssist(
                position_hint=str(obj.get("position_hint", "")),
                probe_question=obj.get("probe_question"),
                next_step=str(obj.get("next_step", "")),
                exercise_prompt=str(obj.get("exercise_prompt", "")),
            )
        except Exception:
            return _fallback.assist_orientation(goal_intent)

    def feedback_on_attempt(
        self,
        *,
        goal_intent: str,
        next_step: str,
        exercise_prompt: str,
        attempt_text: str,
        force_uncertain: bool = False,
    ) -> FeedbackResult:
        if _CODEGEN_RE.search(attempt_text):
            return _fallback.feedback_on_attempt(
                goal_intent=goal_intent,
                next_step=next_step,
                exercise_prompt=exercise_prompt,
                attempt_text=attempt_text,
                force_uncertain=force_uncertain,
            )
        if force_uncertain:
            return _fallback.feedback_on_attempt(
                goal_intent=goal_intent,
                next_step=next_step,
                exercise_prompt=exercise_prompt,
                attempt_text=attempt_text,
                force_uncertain=True,
            )
        try:
            raw = self._chat(
                "Honest coding tutor. Reply JSON: body (string), uncertain (bool). "
                "If unsure, uncertain=true and say so honestly; never fake authority. "
                "Never write a whole project as main value. Chinese.",
                f"goal={goal_intent}\nnext_step={next_step}\n"
                f"exercise={exercise_prompt}\nattempt={attempt_text}",
            )
            m = re.search(r"\{.*\}", raw, re.S)
            obj = json.loads(m.group(0) if m else raw)
            return FeedbackResult(
                body=str(obj.get("body", raw)),
                uncertain=bool(obj.get("uncertain", False)),
            )
        except Exception:
            return FeedbackResult(
                body=(
                    "坦诚边界：外部模型调用失败或结果不可用。"
                    "请稍后重试，或把练习缩小后再提交。"
                ),
                uncertain=True,
            )
