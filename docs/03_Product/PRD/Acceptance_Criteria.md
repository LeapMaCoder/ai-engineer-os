---
title: MVP Acceptance Criteria
type: product
status: draft
owner: ""
created: 2026-07-21
updated: 2026-07-23
tags:
  - prd
  - acceptance
  - mvp
  - leapma
review: founder_pending
quality_pass: "2026-07-21-focus-review"
---

# Acceptance Criteria — 用户价值闭环验收

> 验收：**用户完成了什么价值闭环**，不是页面/控件是否存在。  
> 禁止 UI/线框/交互描述。  
> 对齐核心 **5** 条 User Story / **5** 条 Must AC。

**Must 确认：** Acceptance Criteria = **5**（AC-01…AC-05）

---

## AC-01 用户获得明确下一步（US-01）

| 字段 | 内容 |
|------|------|
| 价值闭环 | 用户从「不知道练什么」→「能陈述接下来最该做的一步」 |
| 准则 | Given 用户带着模糊或大致学习方向进入，When 完成最小定向（含必要的目标澄清与轻量位置感），Then 用户能主动说出下一步学习行动是什么，且该步与其目标相关。 |
| 用户问题 | Primary / SP-1 |
| Growth Loop | GL-1 / GL-2（最小）→ **GL-3** |
| 成功指标 | Activation；路径护栏 |
| 优先级 | Must |

---

## AC-02 用户完成行动并得到可信反馈（US-02）

| 字段 | 内容 |
|------|------|
| 价值闭环 | 用户从「盲目练/不敢练」→「练完知道对错与改进点」 |
| 准则 | Given 用户已有明确下一步，When 完成一次可在单次会话内结束的学习行动，Then 用户获得可理解的反馈（对错或改进点）；若系统不确定，用户得到坦诚边界而非伪造权威。 |
| 用户问题 | Primary / SP-2 |
| Growth Loop | **GL-4 + GL-5** |
| 成功指标 | Activation；WEGS；Learning；无帮助反馈护栏 |
| 优先级 | Must |

---

## AC-03 用户感到进展并知道为何再来（US-03）

| 字段 | 内容 |
|------|------|
| 价值闭环 | 用户从「忙了白忙」→「感到朝目标前进，并知道下次继续什么」 |
| 准则 | Given 用户完成至少一轮「下一步→行动→反馈」，When 回顾本轮，Then 用户能指出相对目标的至少一点具体进展，并能说明下一次回来要继续的方向（下一小步或下一目标）。 |
| 用户问题 | SP-3 |
| Growth Loop | **GL-6 + GL-7 + GL-8** |
| 成功指标 | Retention；Learning Effect；WEGS |
| 优先级 | Must |

---

## AC-04 未付费用户跑通最小闭环（US-04）

| 字段 | 内容 |
|------|------|
| 价值闭环 | 用户从「怀疑要先付钱才有用」→「免费也能完成定向→反馈→进展」 |
| 准则 | Given 用户未付费，When 走完 US-01～US-03（及课内 US-05 最小路径）的最小路径，Then 主价值闭环全部可完成；不出现因未付费而无法获得下一步或可信反馈或进展感知的情况。 |
| 用户问题 | 原则 9 / 信任 |
| Growth Loop | GL-1…GL-8 最小路径 |
| 成功指标 | Retention；Monetization Signal 基础 |
| 优先级 | Must |

---

## AC-05 用户经情境引导先建模再通过验收（US-05）

| 字段 | 内容 |
|------|------|
| 价值闭环 | 用户从「一上来裸做题/听不懂教材腔」→「在情境中建立心智模型后再验收」 |
| 准则 | Given 用户进入 ready 单课，When 完成【学】（正常或故事呈现）再进入验收题并提交，Then 用户能先获得与本课知识点一致的心智模型，再完成可判定练习；概念模式不影响判定对错；不出现联赛/XP 商店/排行等经济系统冒充学习。细则与可测子项见 [[features/SPEC-GL-002_NPC_Guided_Lesson]]（AC-GL2-01…05）。 |
| 用户问题 | SP-2 / 坚持（先懂再练） |
| Growth Loop | **GL-4 + GL-5** |
| 成功指标 | Learning；Activation；Q-A8 |
| 优先级 | Must |
| 决策 | D-056 |

---

## Later AC（不进入本 MVP Must）

| AC | 对应 | 说明 |
|----|------|------|
| AC-L01 | US-L01 | 增强价值可理解且不强迫；仅观察 WTP Signal |

---

## 验收总表（Must）

| AC | 价值一句话 | GL | 指标 |
|----|------------|-----|------|
| AC-01 | 知道下一步 | GL-3（主） | Activation |
| AC-02 | 行动 + 可信反馈 | GL-4/5 | Activation / Learning |
| AC-03 | 进展可见并续环 | GL-6/7/8 | Retention / Learning |
| AC-04 | 免费跑通最小环 | 整环 | Retention |
| AC-05 | 情境建模再验收 | GL-4/5 | Learning |

## Founder Review

- [ ] 5 条 AC 是否都是价值语言？  
- [ ] AC-05 是否误含 UI 描述？  

## 相关文档

- [[User_Stories]] · [[MVP_Core_Problem]] · [[features/SPEC-GL-002_NPC_Guided_Lesson]] · [[Phase3_PRD_Review_Report]]
