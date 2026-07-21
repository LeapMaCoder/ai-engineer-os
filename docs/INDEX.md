---
title: LeapMa 文档索引
type: project
status: active
owner: ""
created: 2026-07-20
updated: 2026-07-21
tags:
  - index
  - leapma
---

# docs/INDEX — 文档索引

> 全库文档导航。重要文档增删改后必须更新本页，并同步 [[Project_Dashboard]] / [[Project_Map]]。

**默认阅读顺序：** [[Project_Dashboard]] → 本索引 → 下钻专题。

---

## 0. 项目治理 `00_Project/`

| 文档 | 说明 |
|------|------|
| [[Project_Dashboard]] | **总览入口**（阶段/目标/风险/地图） |
| [[Project_Map]] | 目录与文档关系 |
| [[Roadmap]] | Phase 路线图 |
| [[Current_State]] | 产品/技术/决策快照 |
| [[Open_Questions]] | 未决问题清单 |
| [[Decision_Log]] | Phase 0–2 关键产品决策 |

## 1. 愿景 `01_Vision/`

| 文档 | 说明 |
|------|------|
| [[LeapMa_Vision]] | 使命愿景用户痛点差异化 |
| [[Product_Principles]] | 产品决策原则（含原则 9/10：成长先于变现、禁止问卷墙） |
| [[Product_North_Star]] | NSM = WEGS |

## 2. 调研 `02_Research/`

### User

| 文档 | 说明 |
|------|------|
| [[Target_User_Analysis]] | 三类用户分析 |
| [[User_Persona_Template]] | 画像模板 |
| [[Problem_Hypothesis]] | 问题假设叙述 |

### User_Interview

| 文档 | 说明 |
|------|------|
| [[Interview_Plan]] | 访谈计划 |
| [[Interview_Template]] | 记录模板 |
| [[Hypothesis_Validation]] | H1–H8 台账 |
| [[Founder_Interview_Guide]] | 创始人话术 |

### Competitors

| 文档 | 说明 |
|------|------|
| [[Boot_dev]] / [[Duolingo]] / [[LeetCode]] / [[Codecademy]] | 留存分析 |
| [[Competitor_Retention_Synthesis]] | 综评 |

### Market

| 文档 | 说明 |
|------|------|
| [[AI_Native_Learning_Opportunity]] | AI Native 机会 |

## 3. 产品 `03_Product/`

| 文档 | 说明 |
|------|------|
| [[ICP_Decision_Framework]] | 首发 ICP 方法 |
| [[MVP/README]] | MVP 包（Phase 2 定稿） |
| [[Python_Track_Outline]] | Python 15 章骨架 + 前三章 ready（D-042/044/047） |
| [[PRD/README]] | **Phase 3 MVP PRD Complete**（`946235b`） |

## 4. 规格 `04_Specifications/`

| 文档 | 说明 |
|------|------|
| [[04_Specifications/README]] | Spec 在 SDD 中的角色 |
| [[Spec_Template]] | Feature Spec 执行模板 |
| [[Feature_Index]] | 索引（SPEC-GL-001 = **Approved**） |
| [[Spec_Status]] | Draft→Review→Approved→Implemented |
| [[features/SPEC-GL-001_First_Growth_Experience]] | **First Growth Experience（Approved）** |

## 5. 架构 `05_Architecture/` · ADR `06_ADR/`

| 文档 | 说明 |
|------|------|
| [[05_Architecture/README]] | 架构目录职责 |
| [[SPEC-GL-001_Architecture]] | First Growth Experience 最小架构（**Approved**） |
| [[Development_Environment]] | 已有环境（≠ 强制栈） |
| [[06_ADR/README]] | ADR 索引 |
| [[ADR-0001_Runtime_Stack_for_SPEC-GL-001]] | 运行时（**Accepted**：Python） |
| [[ADR-0002_Primary_Store_for_SPEC-GL-001]] | 主存（**Accepted**：MySQL） |
| [[ADR-0003_Flask_SSR_for_SPEC-GL-001]] | Web 框架（**Accepted**：Flask SSR） |

## 6–11. 工程文档（占位）

| 目录 | 状态 |
|------|------|
| `07_Sprint/` | 空 |
| `08_Development/` | [[Development_Workflow]] · [[AI_Team_Roles]] |
| `09_Testing/` | 空 |
| `10_Release/` | 空 |
| `11_Operations/` | 空 |
| `templates/` | 通用模板；Feature Spec 以 04 为准 |
| `Archive/` | 空 |

## 仓库其他入口

| 路径 | 说明 |
|------|------|
| [根 README](../README.md) | 人类仓库入口 |
| [.cursor/rules](../.cursor/rules/README.md) | AI 规则索引 |
| [CHANGELOG](../CHANGELOG.md) | 变更日志 |
