---
title: Architecture 索引
type: architecture
status: active
created: 2026-07-21
updated: 2026-07-21
tags:
  - architecture
  - leapma
---

# 05_Architecture — 架构目录

## 职责

描述系统**如何**实现已批准的 Specification。

```text
Vision → Product → Specification → Architecture → Code → Test
```

## 本阶段范围（Phase 5）

| 项 | 状态 |
|----|------|
| 覆盖 Spec | [[features/SPEC-GL-001_First_Growth_Experience]] **Approved** |
| Architecture | [[SPEC-GL-001_Architecture]] **Approved** |
| ADR | ADR-0001 / ADR-0002 **Accepted** |
| 业务代码 | **仍禁止**，直至 Founder **显式授权**垂直切片 |
| 微服务 / K8s / PHP 主栈 | **禁止** |

## 本目录文件

| 文件 | 说明 |
|------|------|
| [[SPEC-GL-001_Architecture]] | First Growth Experience 最小架构（**Approved**） |
| [[Development_Environment]] | Founder 已有环境（≠ 强制技术栈） |
| `docs/06_ADR/` | ADR-0001/0002 **Accepted** |

## 规则

- Architecture **必须**可追溯到 Spec（本阶段 = SPEC-GL-001）。
- 重大选型写 ADR；Accepted 后改栈须新 ADR。
- 环境有什么 ≠ 必须用什么（尤其禁止因有 PHP 默认选 PHP）。
- Diff 越小越好；不为「将来」设计课平台/社区/IDE 等 Hard No 能力。

## 模板

`docs/templates/Architecture_Template.md` · `docs/templates/ADR_Template.md`
