---
title: "ADR-0003: Flask SSR for SPEC-GL-001 web slice"
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

# ADR-0003: Flask + Jinja SSR for SPEC-GL-001 vertical slice

## 状态

**Accepted**（随垂直切片第一刀落地；落实 ADR-0001「不锁框架名」的实现选择）

## 上下文

- ADR-0001 Accepted：Python 单应用，不锁死 Web 框架名。  
- AQ-001：简单 Web，服务端渲染优先；非复杂 SPA。  
- 需要尽快跑通 SPEC-GL-001 手工验收。

## 决策

垂直切片 Web 层选用 **Flask + Jinja2 SSR**。

- 代码位置：`apps/leapma_web/`  
- 不引入复杂 SPA 前端框架。  
- 更换框架须新 ADR（不静默漂移）。

## 后果

### 正面

- SSR 模板直接对齐价值步骤页面；依赖少、一人可维护  
- 与 Flask 生态文档丰富，启动成本低  

### 负面

- 非异步原生优先；高并发 Later 再评估  
- 模板与路由同应用，需保持模块边界纪律  

## 备选方案

| 备选 | 未选原因 |
|------|----------|
| FastAPI + Jinja | 亦可；本切片优先熟悉的同步 SSR 路径 |
| Django | 对第一刀偏重 |
| 复杂 SPA | 违反 AQ-001 |

## 链接

- [[ADR-0001_Runtime_Stack_for_SPEC-GL-001]]
- [[SPEC-GL-001_Architecture]]
- 应用 README：`apps/leapma_web/README.md`
