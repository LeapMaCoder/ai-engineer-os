---
title: Development Environment
type: architecture
status: active
created: 2026-07-21
updated: 2026-07-21
tags:
  - architecture
  - environment
  - leapma
---

# Development Environment — 已有环境记录

> **环境 ≠ 强制技术栈。**  
> 下列为 Founder 本机/现有能力输入，供 ADR 做约束分析；**不**自动等于选型结论。

## 已有（Confirmed 输入）

| 能力 | 备注 |
|------|------|
| Python | 适 AI 编排 / 脚本 / Web |
| Go | 适后续高性能服务；本切片非必须 |
| Redis | 可用；首切片可暂缓 |
| Nginx | 反代 / TLS |
| PHP | 有环境；**禁止因存在而默认选为 LeapMa 主栈** |
| MySQL | 关系型主存候选 |

## 原则

1. 选型写 ADR（Proposed → Founder Review → Accepted）。  
2. 优先：单人可维护、Docker Compose 友好、服务 SPEC-GL-001 最小环。  
3. 见 [[SPEC-GL-001_Architecture]] · [[ADR-0001_Runtime_Stack_for_SPEC-GL-001]] · [[ADR-0002_Primary_Store_for_SPEC-GL-001]]。
