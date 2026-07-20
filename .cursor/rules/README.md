# Cursor Rules — LeapMa

规则用于引导 Cursor Agent。它们**不**替代 `docs/` Source of Truth。

## 规则域

| 域 | 职责 |
|----|------|
| `global/` | SDD 原则、Monorepo 边界、**文档导航同步** |
| `product/` | 需求清晰度与用户价值；禁止跳过文档直接写代码 |
| `architecture/` | 设计完整性、ADR 要求、禁止静默选型 |
| `backend/` | 服务实现约束（已授权写代码时） |
| `frontend/` | 应用/UI 实现约束（已授权写代码时） |
| `ai/` | AI 导师/Agent 行为与安全约束 |
| `testing/` | 与 Spec 挂钩的质量门禁 |
| `review/` | 合并前必须检查什么 |

### global 规则文件

| 文件 | 说明 |
|------|------|
| `sdd-core.mdc` | SDD 与仓库边界 |
| `document-navigation-rule.mdc` | 重要文档变更同步 Dashboard / Map / INDEX |

## 生效模型

- 具体工作优先匹配窄规则。
- Global 规则始终生效。
- 任何实现规则生效前，先满足 Product / Architecture 规则。

## 权威

若规则与 `docs/` 中已接受文档冲突，**改规则** — 文档仍是 Source of Truth。
