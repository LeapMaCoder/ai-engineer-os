---
title: "Spec Template — LeapMa Feature Spec"
type: specification
status: template
created: 2026-07-21
updated: 2026-07-21
tags:
  - specification
  - template
  - leapma
---

# Spec Template — Feature Spec（执行真源）

> 复制本文件到 `docs/04_Specifications/features/`（或同级）后填写。  
> **禁止 UI 线框。** User Flow 只写用户价值步骤。  
> 状态机见 [[Spec_Status]]。

```yaml
spec_id: SPEC-XXX-000
title: ""
status: Draft   # Draft | Review | Approved | Implemented
owner: ""
created: YYYY-MM-DD
updated: YYYY-MM-DD
```

## Spec ID

`SPEC-___-___`

## Status

Draft | Review | Approved | Implemented

## Problem Reference

- Primary / Supporting：[[MVP_Core_Problem]] …
- 一句话问题复述：

## PRD Reference

- [[MVP_Core_Problem]] / [[User_Stories]] / [[Acceptance_Criteria]] / …

## User Story Reference

- US-__ …

## Growth Loop Mapping（强制）

| GL | 本 Spec 是否服务 | 如何服务 |
|----|------------------|----------|
| GL-1 目标设定 | | |
| GL-2 能力评估 | | |
| GL-3 个性化路径 | | |
| GL-4 学习行动 | | |
| GL-5 AI 反馈 | | |
| GL-6 能力提升 | | |
| GL-7 成长可见 | | |
| GL-8 下一目标 | | |

> 若声称「整环」：说明最小路径覆盖 GL-1…8，**不要**拆成 8 份大 Spec（D-039）。

## Scope

### In Scope

-

### Out of Scope（须对照 Hard No）

- 课平台 / 社区 / 招聘 / IDE / 代码生成 / 复杂游戏：默认排除
-

## User Flow（禁止 UI）

用价值步骤描述，例如：

1. 用户带着目标意图进入  
2. …  
3. 用户获得可陈述的下一步 / 反馈 / 进展  

```mermaid
flowchart LR
  A[步骤A] --> B[步骤B] --> C[步骤C]
```

## Business Rules

| ID | 规则 | 证据级别 |
|----|------|----------|
| BR-001 | | Hypothesis / Confirmed / Unknown |

含：Growth Before Monetization、免费最小闭环可跑通等。

## AI Behavior（若涉及反馈）

| ID | 允许 | 禁止 | 不确定时 |
|----|------|------|----------|
| AI-001 | | 幻觉充权威、代写整项目当主价值 | 坦诚边界并引导有效下一步 |

## Acceptance Criteria

引用并细化 PRD AC（可测试）：

| AC ID | 准则（价值闭环） | 通过信号 |
|-------|------------------|----------|
| AC-__ | | |

## Edge Cases

-

## Test Mapping

| Spec / AC | 测试类型（未来） | 备注 |
|-----------|------------------|------|
| | 手工 / 自动 / 评估 | 本阶段不写自动化代码 |

## Open Questions

-

## Future Extension

- 明确 Later，不进入本 Spec Approved 范围

## 变更记录

| 日期 | 变更 | 作者 |
|------|------|------|
| | | |
