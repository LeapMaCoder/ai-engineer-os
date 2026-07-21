# tests/

不属于单一 app 或 service 的跨切面自动化测试。

## 职责

- 覆盖多组件的集成、端到端、契约与冒烟测试。
- 单元测试通常放在被测代码旁：`apps/`、`services/` 或 `packages/`。

## 规则

- 测试跟随 Specification：被测行为须先被规格化。
- 大规模测试套件引入前，先在 `docs/09_Testing/` 写清策略。
- 未经过 Architecture / ADR，不定测试框架选型。

## 状态

Phase 0 占位。尚无测试套件。
