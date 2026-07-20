# 04_Architecture

## 职责

描述系统**如何**实现已批准的 Specification。

Architecture 位于 Spec 与 Code 之间：

Vision → Product → Specification → **Architecture** → Code → Test

## 包含

- 系统上下文与容器图
- 服务 / 应用边界
- 数据流与信任边界
- AI Agent 拓扑（相关时）
- 横切关注点（认证授权、可观测性、多租户等）的设计层描述

## 规则

- Architecture 必须映射到 Specification（可追溯）。
- 重大选型须在 `05_ADR/` 写 ADR。
- 不要在聊天里随口定栈 — 记入本文档 + ADR。
- 禁止无文档更新的「靠 PR 长出架构」。

## 模板

使用 `docs/templates/Architecture_Template.md`。
