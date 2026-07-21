---
title: Decision Log
type: project
status: active
owner: ""
created: 2026-07-21
updated: 2026-07-21
tags:
  - project
  - decisions
  - leapma
---

# Decision Log — 关键产品决策记录

记录 Phase 0–2 已采纳的关键产品 / 流程决策。  
技术选型类决策仍走 `06_ADR/`（尚未启用）。

格式：日期 · 决策 · 状态 · 依据

---

## Phase 0 — 研发体系

| ID | 日期 | 决策 | 状态 | 依据 |
|----|------|------|------|------|
| D-001 | 2026-07-20 | 采用 SDD（规格驱动开发）；docs 为 Source of Truth | Accepted | 项目初始化 |
| D-002 | 2026-07-20 | Monorepo 结构：apps / services / packages / infrastructure / docs | Accepted | Phase 0 |
| D-003 | 2026-07-20 | 禁止无 Product+Spec 的功能开发；重要决策记 ADR | Accepted | SDD / Cursor Rules |
| D-004 | 2026-07-20 | GitHub 仓库名 `ai-engineer-os`；本地置于 `LeapMa/ai-engineer-os/` | Accepted | 仓库对齐 |
| D-005 | 2026-07-21 | docs 编号：`00_Project`，`01_Vision`…`11_Operations`（消除双 00） | Accepted | 目录治理 |

---

## Phase 1 — 愿景与原则

| ID | 日期 | 决策 | 状态 | 依据 |
|----|------|------|------|------|
| D-010 | 2026-07-20 | LeapMa = AI Native 程序员成长平台，非课超市 | Accepted | [[LeapMa_Vision]] |
| D-011 | 2026-07-20 | 核心价值：成长反馈 + 个性化路径 + 长期坚持 | Accepted | Vision |
| D-012 | 2026-07-20 | NSM = WEGS（周有效成长会话） | Accepted | [[Product_North_Star]] |
| D-013 | 2026-07-20 | 产品原则 1–8 生效（成长/反馈/路径/可见/坚持/诚实 AI/垂直/可感知） | Accepted | [[Product_Principles]] |

---

## Phase 1.5–1.7 — 研究与治理

| ID | 日期 | 决策 | 状态 | 依据 |
|----|------|------|------|------|
| D-020 | 2026-07-20 | 调研结论强制标注 Confirmed / Hypothesis / Unknown | Accepted | Research 纪律 |
| D-021 | 2026-07-20 | 竞品分析聚焦留存回路，非功能罗列 | Accepted | Competitors |
| D-022 | 2026-07-20 | 建立 Project Dashboard / Map / Roadmap / State / Questions | Accepted | Phase 1.7 |
| D-023 | 2026-07-21 | User Research = Continuous Validation，**不是** MVP 开发阻塞 | Accepted | Founder Review |

---

## Phase 2 — MVP & Growth Model（定稿）

| ID | 日期 | 决策 | 状态 | 依据 |
|----|------|------|------|------|
| D-030 | 2026-07-21 | Phase 2 MVP 整体方向通过 | Accepted | Founder Review |
| D-031 | 2026-07-21 | **原则 9：Growth Before Monetization** 正式生效 | Accepted | Founder 定稿 |
| D-032 | 2026-07-21 | Freemium：健康免费跑通整环；付费增强效率/深度/个性化，禁止残缺锁成长 | Accepted | [[Free_vs_Paid_Strategy]] |
| D-033 | 2026-07-21 | **Core Growth Loop v1.0** 定为 MVP 产品真源；未来功能必须映射 GL-1…GL-8 | Accepted | [[Core_Growth_Loop]] |
| D-034 | 2026-07-21 | 成长环为八步目标驱动环（目标→…→下一目标） | Accepted | Founder Review |
| D-035 | 2026-07-21 | 成功指标含 Acquisition / Activation / Retention / Monetization Signal / Conversion / Learning Effect | Accepted | [[Success_Metrics]] |
| D-036 | 2026-07-21 | Monetization Signal 含升级兴趣、高级能力需求、价值感知、**Willingness To Pay Signal**；早期不要求付费 | Accepted | Founder 定稿 |
| D-037 | 2026-07-21 | 不假设用户一定付费 | Accepted | 研究/商业纪律 |
| D-038 | 2026-07-21 | Phase 2 定稿完成；下一阶段 = MVP PRD Definition | Accepted | Phase 2 Finalization |
| D-039 | 2026-07-21 | **MVP validates growth loop, not feature completeness** — LeapMa MVP 的目标不是构建完整学习平台，而是验证用户是否能通过成长闭环持续获得价值。Primary Problem 与 4 US / 4 AC 定稿；Hard No 保留。 | Accepted | Phase 3 Final Review |
| D-040 | 2026-07-21 | **首体验去问卷化（方案 1）**：首屏教练对话非测评；探针默认跳过，仅极度模糊时建议且可跳过；尽快 NextStep→短练习。AC 不削弱。 | Accepted | Founder |

---

## 待决（未写入 Accepted）

见 [[Open_Questions]]：ICP 最终锁定、价格带、技术栈等仍 Open。

## 变更规则

新增 Accepted 决策时：更新本文件 + [[Project_Dashboard]]（若影响阶段）+ [[docs/INDEX]]（若新文档）。
