---
title: Specifications 索引
type: specification
status: active
created: 2026-07-21
updated: 2026-07-21
tags:
  - specification
  - sdd
  - leapma
---

# 04_Specifications — 规格体系

> 目录名必须为 **`04_Specifications/`（复数）**。禁止使用 `04_Specification/`。

## Spec 在 SDD 中的位置

```text
Vision → Product → Specification → Architecture → Code → Test
愿景 → 产品 → 规格 → 架构 → 代码 → 测试
```

| 层级 | 回答什么 | 本目录角色 |
|------|----------|------------|
| Vision / Principles | 为什么、原则 | 上游约束 |
| Product / PRD | 解决谁的什么问题 | 上游真源 |
| **Specification** | **可测试的行为契约** | **本目录** |
| Architecture / ADR | 如何实现 | 下游（尚未启用技术选型） |
| Code / Test | 实现与证明 | 更下游；Approved 前禁止实现 |

## Spec 是什么

- **可测试契约**：写清行为与验收，模糊即缺陷。
- **必须引用**：PRD / User Story / Acceptance Criteria。
- **必须映射**：Growth Loop **GL-1…GL-8**（或显式声明服务哪些环节）。
- **必须遵守**：Hard No、原则 9 Growth Before Monetization、**D-039**（验证成长闭环，非功能完整）。
- **状态机入口**：见 [[Spec_Status]]（Draft → Review → Approved → Implemented）。

## 产品约束（写 Spec 时）

| 约束 | 含义 |
|------|------|
| Growth Before Monetization | 不写残缺免费逼付费的行为 |
| GL 映射强制 | 无 GL 映射的 Spec 不得 Approved |
| D-039 | 第一刀验证闭环，不追求平台完整 |
| Hard No | 课平台 / 社区 / 招聘 / IDE / 代码生成 / 复杂游戏 |
| 禁止八拆 | **禁止**按 GL 拆成 8 个大 Spec；第一刀为整环 [[Feature_Index\|SPEC-GL-001]] |

## 本目录文件

| 文件 | 说明 |
|------|------|
| [[Spec_Template]] | **写 Feature Spec 用此模板**（LeapMa 执行模板） |
| [[Feature_Index]] | Feature Spec 索引与状态 |
| [[Spec_Status]] | 状态机与门禁规则 |
| `features/` | Feature Spec 正文（如 [[features/SPEC-GL-001_First_Growth_Experience]]） |
| `docs/templates/Specification_Template.md` | 通用 SDD 草稿模板（Obsidian/历史） |

### 双模板关系（避免双真源）

| 模板 | 用途 |
|------|------|
| **`04_Specifications/Spec_Template.md`** | **唯一执行真源**：新建/评审 Feature Spec 必须用此结构 |
| `docs/templates/Specification_Template.md` | 通用占位/早期 SDD 模板；**不**再作为 Feature Spec 正文来源 |

若二者冲突：以 `04_Specifications/Spec_Template.md` + 已 Approved 的 Feature Spec 为准。

## 当前阶段

**Phase 4** — Spec 基建就绪；**SPEC-GL-001 First Growth Experience = Approved**。

下一步：Architecture。仍禁止无 Arch 的业务代码；本任务不 commit。
