"""LLM Provider interface — replaceable (AQ-002)."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional


@dataclass
class FeedbackResult:
    body: str
    uncertain: bool = False
    rejected_codegen: bool = False


@dataclass
class OrientationAssist:
    position_hint: str
    probe_question: Optional[str]
    next_step: str
    exercise_prompt: str


class LLMProvider(ABC):
    """Swap implementations via LEAPMA_LLM_PROVIDER without locking a vendor."""

    @abstractmethod
    def assist_orientation(self, goal_intent: str) -> OrientationAssist:
        ...

    @abstractmethod
    def feedback_on_attempt(
        self,
        *,
        goal_intent: str,
        next_step: str,
        exercise_prompt: str,
        attempt_text: str,
        force_uncertain: bool = False,
    ) -> FeedbackResult:
        ...


def get_provider(name: str) -> LLMProvider:
    key = (name or "mock").strip().lower()
    if key == "mock":
        from leapma_web.llm.mock import MockProvider

        return MockProvider()
    if key in ("openai_compatible", "openai", "compatible"):
        from leapma_web.llm.openai_compatible import OpenAICompatibleProvider

        return OpenAICompatibleProvider()
    raise ValueError(f"Unknown LEAPMA_LLM_PROVIDER: {name}")
