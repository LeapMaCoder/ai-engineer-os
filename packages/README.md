# packages/

Monorepo 的共享库与契约。

## 职责

- 供 `apps/` 与 `services/` 复用的代码（类型、UI 原语、工具、客户端等）。
- 在真实出现多处消费者后再抽取，降低重复。

## 规则

- 遵循三次原则（Rule of Three）：没有真实复用前不要抽包。
- Phase 0 不定包结构与技术栈。
- 包不得依赖 `apps/` 或 `services/`（依赖方向指向 packages）。

## 状态

Phase 0 占位。尚未创建任何包。
