"""Mock LLM — deterministic path for AC walkthrough without API keys."""

from __future__ import annotations

import re

from leapma_web.llm import FeedbackResult, LLMProvider, OrientationAssist

_CODEGEN_RE = re.compile(
    r"(整(个)?项目|完整项目|帮我写完|直接生成.*(代码|项目)|代写.*项目)",
    re.I,
)


class MockProvider(LLMProvider):
    def assist_orientation(self, goal_intent: str) -> OrientationAssist:
        g = goal_intent.strip() or "提升编程能力"
        return OrientationAssist(
            position_hint=(
                f"听起来你想推进「{g}」。我先假设你有方向、还缺一个能立刻动手的小步——"
                "我们直接练，不搞测评。"
            ),
            probe_question=(
                f"若方便多说一句：相对「{g}」，你更卡在「概念」还是「动手」？"
                "（可跳过）"
            ),
            next_step=(
                f"下一步：完成一道与「{g}」相关的短练习（几分钟内可做完），"
                "然后根据反馈改一处。"
            ),
            exercise_prompt=(
                f"短练习：用你自己的话写 3～5 句，说明「{g}」里你今天只攻克的一个小点；"
                "或写一段伪代码/步骤。不要要求系统代写整个项目。"
            ),
        )

    def feedback_on_attempt(
        self,
        *,
        goal_intent: str,
        next_step: str,
        exercise_prompt: str,
        attempt_text: str,
        force_uncertain: bool = False,
    ) -> FeedbackResult:
        text = attempt_text.strip()
        if _CODEGEN_RE.search(text):
            return FeedbackResult(
                body=(
                    "这更像「代写整个项目」请求，不是本产品的主价值（Hard No）。\n"
                    "请回到与目标相关的短练习：只提交一小段可改错的内容，"
                    "我会指出对错与改进点。"
                ),
                rejected_codegen=True,
            )
        if force_uncertain or "不确定演示" in text or text.lower() == "idk":
            return FeedbackResult(
                body=(
                    "坦诚边界：根据你提交的内容，我无法可靠判断对错"
                    "（信息不足或超出我能确定的范围）。\n"
                    "有效下一步：把练习缩小为「一个具体概念 + 一句你的理解」，再提交一次。"
                ),
                uncertain=True,
            )
        if len(text) < 20:
            return FeedbackResult(
                body=(
                    "改进点：回答偏短，还看不出相对目标的具体理解。\n"
                    "请补充：你攻克的小点是什么、为什么和目标相关。"
                ),
                uncertain=False,
            )
        return FeedbackResult(
            body=(
                f"相对目标「{goal_intent}」：你的提交表明你已尝试用自己的话落地下一步。\n"
                "对的地方：有具体表述，不是空泛口号。\n"
                "改进点：下次把「可观察的改错点」写得更明确（错在哪、改哪一句）。"
            ),
            uncertain=False,
        )
