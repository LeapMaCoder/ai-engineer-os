---
title: LeapMa 项目仪表盘
type: project
status: active
owner: ""
created: 2026-07-20
updated: 2026-07-23
tags:
  - project
  - dashboard
  - leapma
---

# Project Dashboard — 项目总览

最后更新：`2026-07-23`

---

## 1. 项目当前阶段

| 项 | 值 |
|----|-----|
| **阶段** | **Phase 5 — 视觉 + 游客 Dashboard + Python 15 章骨架** |
| **体验** | D-048 暗色终端；D-049～051 先学后练 + story；**D-057** 跃迁站四 NPC（墨狸/回响/闸/跃）；**D-056/GL-002**；**D-058** MySQL 中文 COMMENT；Python 1～3 ready |

---

## 2. 当前目标

1. 走通 Python **第 1～3 章**混合题型 + Dashboard / profile 分工  
2. 对齐 **D-056 / D-057 / SPEC-GL-002**（四 NPC 叙事型坚持）与 **D-058**（MySQL COMMENT）  
3. 试用验证 **Q-A8**（normal vs story）  
4. **不自动 commit**  

---

## 3. 已完成（摘）

| 项 | 入口 |
|----|------|
| 原则 10 / D-040…056 | [[Product_Principles]] · [[Decision_Log]] |
| SPEC-GL-001 / GL-002 | [[Feature_Index]] |
| 应用 | `apps/leapma_web` |
| 大纲 | [[Python_Track_Outline]] |

---

## 4. 风险（当前）

| 风险 | 缓解 |
|------|------|
| 叙事滑向视觉小说 / 长分叉 | D-056 Out；Hard No 复杂游戏 |
| 文档与实现漂移 | Spec 真源；改行为先改 Spec |

---

## 5. Review

- [ ] Founder Review：**D-056 / SPEC-GL-002 / US-05 / AC-05** 文档债  
- [ ] 第 1～3 章手工 / `uv run python test_client.py` 冒烟  
- [ ] **不要由 Agent commit**  
