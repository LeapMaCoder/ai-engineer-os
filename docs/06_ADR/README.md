---
title: 06_ADR — 架构决策记录
type: adr
status: active
created: 2026-07-21
updated: 2026-07-21
tags:
  - adr
  - leapma
---

# 06_ADR — 架构决策记录

## 职责

记录**重要技术决策**及其理由，避免未来人类与 AI Agent 默默推翻。

## 状态取值

Proposed | Accepted | Deprecated | Superseded

## 当前 ADR

| ID | 标题 | 状态 |
|----|------|------|
| [[ADR-0001_Runtime_Stack_for_SPEC-GL-001]] | Runtime stack for SPEC-GL-001 | **Accepted** |
| [[ADR-0002_Primary_Store_for_SPEC-GL-001]] | Primary store for SPEC-GL-001 | **Accepted** |
| [[ADR-0003_Flask_SSR_for_SPEC-GL-001]] | Flask + Jinja SSR 实现选择 | **Accepted** |

## 规则

- 追加式：用新 ADR 废止旧决策，勿改写历史。  
- 链接 Architecture 与 Spec。  
- Arch + 必要 ADR **Accepted** 后，仍须 Founder **显式授权**才可写业务功能代码。

## 模板

`docs/templates/ADR_Template.md`
