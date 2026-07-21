---
title: LeapMa 项目仪表盘
type: project
status: active
owner: ""
created: 2026-07-20
updated: 2026-07-21
tags:
  - project
  - dashboard
  - leapma
---

# Project Dashboard — 项目总览

最后更新：`2026-07-21`

---

## 1. 项目当前阶段

| 项 | 值 |
|----|-----|
| **阶段** | **Phase 5 — Vertical Slice 进行中（SPEC-GL-001）** |
| **SDD** | Spec ✅ → Arch ✅ → **Code 🔄** → Test ⏳ |

```mermaid
flowchart LR
  Auth[Founder 授权 ✅] --> Slice[leapma_web 🔄]
  Slice --> AC[手工验收 AC-01…04]
```

---

## 2. 当前目标

1. 验收去问卷化后的首体验（方案 1 / D-040）  
2. 跑通 AC-01…04（探针非默认路径）  
3. **不自动 commit**  

---

## 3. 已完成

| 项 | 入口 |
|----|------|
| Spec / Arch / ADR | Approved / Accepted |
| 垂直切片 | `apps/leapma_web` |
| **D-040 去问卷化** | 首屏单输入教练对话；探针仅极度模糊且可跳过 |

---

## 4. 进行中

| 事项 | 状态 |
|------|------|
| SPEC-GL-001 垂直切片 | **实现已落地；待本地验收 / Founder commit** |

---

## 5. 下一步

| 顺序 | 行动 |
|------|------|
| 1 | 按 app README 启动并用 Mock 走通 AC |
| 2 |（可选）接 MySQL + openai_compatible |
| 3 | Founder 手动 commit |

---

## 6. Review

- [x] Founder 显式授权编码  
- [ ] 手工验收通过  
- [ ] **不要由 Agent commit**  
