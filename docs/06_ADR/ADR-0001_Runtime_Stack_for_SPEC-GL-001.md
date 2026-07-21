---
title: "ADR-0001: Runtime stack for SPEC-GL-001"
type: adr
status: accepted
owner: ""
created: 2026-07-21
updated: 2026-07-21
tags:
  - adr
  - leapma
supersedes: ""
superseded_by: ""
---

# ADR-0001: Runtime stack for SPEC-GL-001 vertical slice

## 状态

**Accepted**（Founder 2026-07-21）

## 上下文

- Spec：[[features/SPEC-GL-001_First_Growth_Experience]] Approved；需 AI 编排（定向推断、反馈、不确定分支）。
- 约束：单人可维护；Docker Compose 友好；D-039 验证闭环非平台。
- 环境输入：Python / Go / Redis / Nginx / PHP / MySQL（见 [[Development_Environment]]）。
- **禁止**因有 PHP 默认选 PHP。
- UI：简单 Web、服务端渲染优先（见 Architecture AQ-001）。

## 决策

**以 Python 为 SPEC-GL-001 垂直切片的主运行时**，单应用承载 Web 入口（SSR 优先）+ AI 编排。

- **不锁**具体 Web 框架名（实现阶段再选，须符合 SSR 优先）。  
- Go：**不**作为本切片主栈；保留为后续独立服务选项。  
- PHP：**不**作为本切片主栈。  
- 部署形态：单进程/单服务优先；Nginx 可选反代。
## 后果

### 正面

- Python 生态利于 LLM SDK、提示与评估脚本；迭代快，贴合 GL-5 主战场  
- 单应用减少分布式复杂度（反微服务）  
- 与 Founder 已有 Python 环境对齐  

### 负面

- 高并发/强类型边界不如 Go 天然；若流量起来需再评估（Later）  
- 需纪律防止「脚本堆」侵蚀模块边界  

### 中性

- Nginx / Redis 仍可按需接入，不绑定本决策  

## 备选方案

| 备选 | 利 | 弊 | 未选原因（建议） |
|------|----|----|------------------|
| **A. Python 单应用（建议）** | AI 编排快；一人可维护；Compose 简单 | 需自律模块边界 | — |
| **B. Go 单应用** | 性能/部署清晰 | AI 编排与评测工具链不如 Python 顺；首切片慢 | 首切片主成本在 AI 行为非 QPS |
| **C. PHP 单应用** | 环境已有 | AI 编排与团队长期方向弱；易滑向传统站 | 禁止环境默认；不贴 Spec 主成本 |
| **D. Python API + Go 服务拆分** | 边界清晰 | 过早微服务；运维倍增 | 违反本阶段最小原则 |
| **E. 纯静态前端 + 无后端** | 极简 | 无法可靠落 Feedback 边界与持久化进展 | 不满足 AC |

## 链接

- Architecture：[[SPEC-GL-001_Architecture]]
- Spec：[[features/SPEC-GL-001_First_Growth_Experience]]
- 相关 ADR：[[ADR-0002_Primary_Store_for_SPEC-GL-001]]
