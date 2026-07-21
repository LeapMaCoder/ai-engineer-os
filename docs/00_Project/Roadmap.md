---
title: 产品路线图
type: project
status: active
owner: ""
created: 2026-07-20
updated: 2026-07-21
tags:
  - project
  - roadmap
  - leapma
---

# Roadmap — 阶段路线图

> 路线图描述**阶段目标**，不是功能 backlog。  
> 未完成上游门禁前，禁止跳入编码。

```mermaid
timeline
  title LeapMa 阶段
  Phase 0 : 研发体系
  Phase 1 : 愿景与原则
  Phase 1.5 : 桌面调研
  Phase 1.6 : 用户发现访谈
  Phase 1.7 : 项目治理
  Phase 2 : MVP 与增长模型
  Phase 3 : MVP PRD Complete
  Phase 4 : Spec 与架构
  Phase 5 : 首个垂直切片
  Phase 6+ : 扩展与规模化
```

---

## Phase 0 — 项目初始化与研发体系 ✅

**目标：** AI Native SDD 地基

**完成标志：**

- Monorepo 骨架与目录 README
- docs 体系与模板
- Cursor Rules / AI 角色 / 开发流程
- Git 初始化

**状态：** 完成

---

## Phase 1 — Product Foundation ✅

**目标：** 产品战略真源

**完成标志：**

- [[LeapMa_Vision]]
- [[Product_Principles]]
- [[Product_North_Star]]

**状态：** 完成

---

## Phase 1.5 — Research Validation ✅（桌面）

**目标：** 验证产品假设（桌面层）

**完成标志：**

- 用户分析 / 问题假设
- 竞品留存分析
- AI Native 市场机会文档
- 结论标注 Confirmed / Hypothesis / Unknown

**状态：** 桌面部分完成；**一手验证未完成**（转入 1.6）

---

## Phase 1.6 — Founder User Discovery 🔄

**目标：** 确定 MVP 首发人群

**完成标志：**

- 访谈体系就绪 ✅
- **10 场访谈执行** ⏳
- Hypothesis 台账更新 ⏳
- ICP 决策记录 ⏳

**状态：** 体系完成，执行中/待执行

---

## Phase 1.7 — Project Governance ✅

**目标：** 项目状态对 AI/人类可见

**状态：** ✅ 完成

---

## Phase 2 — MVP & Growth Model Definition ✅

**目标：** 定义第一个 MVP，并同时考虑免费留存与付费转化

**完成标志：**

- `docs/03_Product/MVP/` 文档包
- Freemium 价值差异（非残缺锁功能）
- 成功指标与风险
- Founder Review 通过

**状态：** ✅ 定稿（commit `cca5bd0`）

---

## Phase 3 — MVP PRD Definition ✅

**目标：** 以 Problem First 定义第一个 MVP 要解决的核心用户问题

**完成标志：**

- Primary Problem 定稿
- Must User Stories = 4；Must AC = 4
- Hard No 确认
- D-039：MVP validates growth loop, not feature completeness
- Founder Final Review 方向批准

**状态：** ✅ **MVP PRD Complete**（文档定稿；**等待最终确认后 commit**）

**禁止（仍有效）：** 代码 / 技术架构抢跑 / 数据库 / UI

**下一阶段：** Phase 4 Specification & Architecture

---

## Phase 4 — Specification & Architecture ⏳

**目标：** 在 PRD 批准后，形成可测试规格与系统设计

**进入条件：**

- Phase 3 PRD Founder Review 通过
- 核心假设持续验证中（不要求全部 Confirmed）

**产出（方向）：**

- `04_Specifications/` 核心 Spec
- `05_Architecture/` 系统架构
- `06_ADR/` 必要决策

**禁止提前：** 无 Spec/Arch 的业务编码

**状态：** 未开始

---

## Phase 5 — First Vertical Slice ⏳

**目标：** 首个可验证的垂直切片实现（具体范围以 Spec 为准）

**进入条件：** Phase 4 门禁通过

**产出（方向）：**

- `apps/` / `services/` 最小实现
- 映射 Spec 的测试

**状态：** 未开始

---

## Phase 6+ — Expand & Operate ⏳

**方向（非承诺）：** 图谱深化、护栏内游戏化、多端、运维、NSM 迭代

**状态：** 未开始

---

## 阶段门禁总览

| 从 | 到 | 门禁 |
|----|-----|------|
| Phase 2 | Phase 3 | MVP 策略定稿 |
| Phase 3 | Phase 4 | PRD Founder Review |
| Phase 4 | Phase 5 | Spec + Arch（+ADR） |
| Phase 5 | Release | Review + Test 映射 Spec |

详见 [[Development_Workflow]]。
