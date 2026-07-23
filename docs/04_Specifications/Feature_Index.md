---
title: Feature Spec Index
type: specification
status: active
created: 2026-07-21
updated: 2026-07-23
tags:
  - specification
  - index
  - leapma
---

# Feature Index — Feature Spec 索引

> 只登记索引与状态。**Planned ≠ 已写正文。**  
> 第一刀：整环最小体验，**禁止**按 GL 拆 8 个大 Spec。  
> 课内教学另开 SPEC-GL-002（不拆八环）。

| ID | Name | Status | PRD Reference | Growth Loop Mapping |
|----|------|--------|---------------|---------------------|
| SPEC-GL-001 | First Growth Experience | **Approved** | [[User_Stories]] US-01~04 · [[Acceptance_Criteria]] AC-01~04 · [[MVP_Core_Problem]] | GL-1…GL-8 **最小闭环**（单 Spec） |
| SPEC-GL-002 | NPC Guided Lesson | **Approved** | [[User_Stories]] US-02·US-05 · [[Acceptance_Criteria]] AC-02·AC-05 · D-056 | **GL-4 + GL-5**（单课如何学） |

## 正文入口

| ID | 路径 |
|----|------|
| SPEC-GL-001 | [[features/SPEC-GL-001_First_Growth_Experience]] |
| SPEC-GL-002 | [[features/SPEC-GL-002_NPC_Guided_Lesson]] |

## 状态说明

见 [[Spec_Status]]。当前：SPEC-GL-001 / SPEC-GL-002 = **Approved**。  
架构：GL-001 已有 Arch；GL-002 可复用该 Arch，跨课剧情引擎另开。

## 写作入口

新开正文时：复制 [[Spec_Template]]，改 Status=Draft，放入 `features/`，并更新本表。
