# services/

后端与 AI 运行时服务放在此目录。

## 职责

- 承载 API、Worker、AI Agent 等服务。
- 将可独立部署单元与共享库（`packages/`）、客户端（`apps/`）分离。

## 规则

- 在完成 产品定义 → Specification → Architecture → ADR（必要时）之前，不实现服务。
- 优先清晰的服务边界，避免过早拆成微服务。
- 跨切面契约（类型、OpenAPI、事件等）在 Architecture 决策后，优先沉淀到 `packages/`。

## 状态

Phase 0 占位。尚未创建任何服务。
