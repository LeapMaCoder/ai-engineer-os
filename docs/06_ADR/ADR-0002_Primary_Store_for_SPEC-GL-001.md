---
title: "ADR-0002: Primary store for SPEC-GL-001"
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

# ADR-0002: Primary store for SPEC-GL-001 vertical slice

## 状态

**Accepted**（Founder 2026-07-21）

## 上下文

- 需持久化产品实体：GoalIntent、NextStep、Attempt、Feedback、ProgressNote、NextIntent、UserRef 等（见 [[SPEC-GL-001_Architecture]]）。
- 环境已有 MySQL、Redis。
- 首切片数据量小；需要可查询的会话/进展记录以支撑 AC-03/手工验收。

## 决策

**MySQL 作为 Primary Store。**

- Redis：**不**作为主存；首切片**非必须**（会话缓存/限流 Later）。  
- 本 ADR **不**批准具体 DDL/ORM；表结构属实现任务（须 Founder 授权编码后）。
## 后果

### 正面

- 关系模型清晰表达 Attempt↔Feedback↔GoalIntent  
- Founder 环境已有，Compose 常见  
- 利于手工验收与简单查询  

### 负面

- 需迁移纪律；早期 schema 会变（可接受）  
- 非文档型灵活存储（本切片实体结构化足够）  

### 中性

- 文件/SQLite 可作极早期原型，但与已有 MySQL 相比收益有限  

## 备选方案

| 备选 | 利 | 弊 | 未选原因（建议） |
|------|----|----|------------------|
| **A. MySQL（建议）** | 已有；结构化；够用 | schema 演进成本 | — |
| **B. Redis-only** | 快 | 不适合进展/审计主存；易丢 | 不满足可靠 ProgressNote |
| **C. SQLite 单文件** | 零运维 | 与现有 MySQL 能力重复；多实例弱 | 环境已有 MySQL |
| **D. 仅文档 DB** | 灵活 | 过早；查询/约束弱 | 首切片实体简单，无必要 |
| **E. 无持久化** | 最快 | 无法证明续环与回顾 | 不满足 AC-03 可追溯 |

## 链接

- Architecture：[[SPEC-GL-001_Architecture]]
- Spec：[[features/SPEC-GL-001_First_Growth_Experience]]
- 相关 ADR：[[ADR-0001_Runtime_Stack_for_SPEC-GL-001]]
