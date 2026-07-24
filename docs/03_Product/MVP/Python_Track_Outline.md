---
title: Python Track Outline（初期）
type: product
status: active
created: 2026-07-21
updated: 2026-07-21
tags:
  - mvp
  - python
  - leapma
---

# Python 赛道大纲（15 章骨架 · 前三章可玩）

> **原创声明**：课文与习题由 LeapMa **改写**自 Founder 的 Engineer OS Obsidian 笔记（`02 - Learning/Boot.dev/...` Concepts / Drills / Review，以及 Training-Grounds Quiz），**不是** Boot.dev 官网原文粘贴，也不是整份 Markdown 当页面。  
> 决策：D-042 / D-043 / D-044 / **D-047**。原则：禁止问卷墙、Growth Before Monetization、规则判定为主。

## 进度总览

| 章 | 主题 | 状态 |
|----|------|------|
| py-01 | 变量与类型（含极短 print 热身） | **ready**（5 课可判定） |
| py-02 | 函数 | **ready**（5 课） |
| py-03 | 作用域 | **ready**（5 课） |
| py-04 | 导论与路径（Introduction） | skeleton |
| py-05 | 测试与调试 | skeleton |
| py-06 | 计算 | skeleton |
| py-07 | 比较 | skeleton |
| py-08 | 循环 | skeleton |
| py-09 | 列表 | skeleton |
| py-10 | 字典 | skeleton |
| py-11 | 集合 | skeleton |
| py-12 | 错误处理 | skeleton |
| py-13 | 类型提示 | skeleton |
| py-14 | 综合练习 | skeleton |
| py-15 | 章末测验 | skeleton |

内容目录：`apps/leapma_web/content/python/`

## 叙事 / NPC 约定（D-056 / D-057）

世界观：**跃迁站 Leap Station**（赛博夜港训练站）。scene 可换工位；说话人只能是下表四人。

| id | 显示名（`story.npc`） | 专治 |
|----|----------------------|------|
| ink | **墨狸** | 绑定 / 类型 / print 热身 |
| echo | **回响** | print vs return、调用交付 |
| gate | **闸** | 作用域 / NameError |
| leap | **跃** | 元教练：收束、跨课钩子、苏格拉底追问 |

| 章 | 幕名 | 主场 |
|----|------|------|
| py-01 | **墨狸的贴签夜** | 墨狸（跃可开场/收束客串） |
| py-02 | **回响的假交货** | 回响为主（跃收束） |
| py-03 | **闸的门外禁区** | 闸为主（跃收束） |

| 约定 | 说明 |
|------|------|
| NPC 池 | 全站固定 **恰好 4**；`content/python/npcs.json` 为名单真源 |
| 每课主 NPC | `concept.story.npc` 必须精确匹配上表显示名 |
| 引导链 | 困境 → 概念 → 例 → 练；先学后练（D-049） |
| 禁止 | 池外具名角色；联赛 / XP 商店 / 排行 / 好感度 / 长分叉 |

细则：[[features/SPEC-GL-002_NPC_Guided_Lesson]]。

## 题源对齐（Obsidian → LeapMa）

| LeapMa | Obsidian 主源 | 题型混合 |
|--------|---------------|----------|
| py-01 | ch01-variables + drill + review + quiz | mcq / fill / short / code |
| py-02 | ch02-functions + drill + review + quiz | mcq / fill / short / code |
| py-03 | ch03-scope + drill + review | mcq / fill / short / code |

## 反馈策略

主路径：**规则判定**（`rules_feedback`，支持 `type: mcq|fill|short|code`）。LLM Provider 保留，默认 mock，**不**作为能跑通前提（D-043）。

## 非目标（本批）

- 不写满第 4～15 章习题  
- 不做真沙箱 Run  
- 不强制注册才能学  
- 不把 Obsidian md 原样挂成页面  
