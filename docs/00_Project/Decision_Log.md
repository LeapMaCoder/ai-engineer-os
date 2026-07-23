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
| D-041 | 2026-07-21 | **原则 10：No Questionnaire Wall（禁止问卷墙）** 正式生效。禁止用多题问卷/测评墙换个性化；价值在前、画像在后；推断优先、提问可跳过且不得阻塞下一步/短练习/反馈。与原则 9、Growth Loop、D-040 / BR-011…013 对齐。 | Accepted | Founder / Strategic |
| D-042 | 2026-07-21 | **初期垂直赛道 = Python 学习成长**（先打穿）；愿景/Hard No/原则不变。 | Accepted | Founder |
| D-043 | 2026-07-21 | **判定式/规则反馈优先**；真实 LLM 为辅（Later）。保留可替换 Provider；默认 mock；不以真实 LLM 为跑通前提。 | Accepted | Founder |
| D-044 | 2026-07-21 | **Boot.dev 式章节动手路径**（窄路径、章内练习→可见对错）；初期 Python **前三章**，可一章一章交付；**禁止抄袭**竞品文本/习题。 | Accepted | Founder |
| D-045 | 2026-07-21 | **成长可见门面**：自有视觉风格 + 游客个人中心 / Dashboard Demo（路线+进度，无强制注册、无复杂游戏化）；Run 沙箱可滞后。 | Accepted | Founder |
| D-046 | 2026-07-21 | **可选账号（非门槛）**：Dashboard 保持游客可用；轻量 username+password 哈希存库；登录后绑定进度/显示名；禁止注册墙。 | Accepted | Founder |
| D-047 | 2026-07-21 | **Python 15 章主题骨架 + 先打穿 1～3 章**：主题序含 Introduction→…→Quiz；ready 对齐 Obsidian ch01 变量 / ch02 函数 / ch03 作用域；题源=Engineer OS 笔记**改编**（禁抄 Boot.dev 官网）；题型 mcq/fill/short/code；规则判定为主；4～15 skeleton 诚实未开放。 | Accepted | Founder |
| D-048 | 2026-07-21 | **视觉迁暗色终端风**：采用 Boot.dev-inspired design tokens（primary `#00FF88` 等）；弱化/不做 XP·商店·排行榜·成就墙；金仅作进度点缀；禁止问卷墙与注册门槛不变。 | Accepted | Founder |
| D-049 | 2026-07-21 | **课内先学后练**：lesson 固定【学】【例】【练】【提交】；内容钩子 `concept.normal` + `concept.story`（ready 课均必填）+ `example`（code/note；示例≠练习）；模式切换不影响判定。 | Accepted | Founder |
| D-050 | 2026-07-22 | **故事模式任务简报**：`concept.story` 升为对象（mission/scene/npc/objective/body…）；UI 壳 `story-mission` 与 normal 明显区分；旧字符串兼容包成 `{body}`；无 XP/商店。 | Accepted | Founder |
| D-051 | 2026-07-22 | **概念模式方案 B**：个人中心默认 `concept_mode_default`（normal\|story）；每次打开/刷新课按默认渲染【学】；课内切换仅临时、不写默认/不写 URL；游客 session+cookie；登录用户 session+DB（账号为准）；无 story 课诚实回退。 | Accepted | Founder |
| D-052 | 2026-07-22 | **个人中心独立页**：`/profile` 管昵称/时间/默认概念模式/进度/可选账号；`/dashboard` 只保留续学+章列表+摘要联动；`/me` → `/profile`；游客可进、无注册墙。 | Accepted | Founder |
| D-053 | 2026-07-23 | **打磨 Python 第 1～3 章内容质量**：润色 normal/story/example；收紧填空判定（防子串误伤）；fail 文案更可执行；不开第 4～15 章。 | Accepted | Founder |
| D-054 | 2026-07-23 | **个人中心信息架构打磨**：`/profile` = 账户与设置（资料/默认模式/进度摘要/账号）；`/dashboard` = 接下来练什么（仅摘要链到 profile）；方案 B 不变。 | Accepted | Founder |
| D-055 | 2026-07-23 | **整体 UI 微调**：统一间距/标题/按钮主次；课内四分区色条更清晰；去掉静态 panel 满屏 hover；故事壳对比加强；不改产品范围。 | Accepted | Founder |

---

## 待决（未写入 Accepted）

见 [[Open_Questions]]：ICP 最终锁定、价格带、技术栈等仍 Open。

## 变更规则

新增 Accepted 决策时：更新本文件 + [[Project_Dashboard]]（若影响阶段）+ [[docs/INDEX]]（若新文档）。
