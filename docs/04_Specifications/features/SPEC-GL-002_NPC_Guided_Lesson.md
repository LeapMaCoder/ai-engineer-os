---
title: "SPEC-GL-002 NPC Guided Lesson"
type: specification
status: approved
owner: ""
created: 2026-07-23
updated: 2026-07-23
tags:
  - specification
  - feature
  - leapma
  - growth-loop
  - npc
spec_id: SPEC-GL-002
---

# SPEC-GL-002 — NPC Guided Lesson（课内 NPC 引导式学习）

```yaml
spec_id: SPEC-GL-002
title: NPC Guided Lesson
status: Approved   # Draft | Review | Approved | Implemented
owner: ""
created: 2026-07-23
updated: 2026-07-23
```

## Spec ID

`SPEC-GL-002`

## Status

**Approved** — 课内「如何学」的产品行为契约。  
**分工：** [[features/SPEC-GL-001_First_Growth_Experience]] = 首次成长**闭环**（定向→行动→反馈→进展）；**本 Spec = 单课内如何先建模再验收**（NPC 引导链）。  
**实现：** 可复用 SPEC-GL-001 Architecture / 现有 SSR 课内结构；跨课剧情引擎 / 状态机若需要，**另开 Architecture**，不塞进本 Spec。  
改行为须先改本 Spec。决策：**D-056**；承接 **D-049～051**。

## Problem Reference

- Primary：[[MVP_Core_Problem]] — 缺路径 + 缺可信反馈 → 不知下一步 / 难坚持  
- Supporting：**先练后懂**导致误伤与放弃；教材腔讲解难以建立可迁移心智模型  
- 一句话：用户进入单课时，应先在情境中建立心智模型，再通过验收题检验，而非一进来就裸做题。

## PRD Reference

- [[User_Stories]]（**US-02**、**US-05**）
- [[Acceptance_Criteria]]（**AC-02**、**AC-05**）
- [[MVP_Out_of_Scope]]（Hard No + 允许边界）
- [[Non_Goals]]
- [[Python_Track_Outline]]（叙事/NPC 约定）
- Decision_Log：**D-056**、**D-049～051**、**D-039**、**D-041**、**D-043**

## User Story Reference

| US | 本 Spec 覆盖 |
|----|--------------|
| US-02 行动并获得可信反馈 | ✅（验收题 = 行动；判定/反馈仍诚实） |
| US-05 情境引导建立心智模型再验收 | ✅ **主** |
| US-01 / US-03 / US-04 | 不本 Spec 主责（见 SPEC-GL-001） |

## Growth Loop Mapping（强制）

| GL | 本 Spec 是否服务 | 如何服务 |
|----|------------------|----------|
| GL-1 目标设定 | — | 不本 Spec |
| GL-2 能力评估 | — | 不本 Spec |
| GL-3 个性化路径 | 轻 | 章/课选择仍属路径；本 Spec 不扩路径引擎 |
| GL-4 学习行动 | ✅ **主** | 学→例→练→提交；练为可判定验收行动 |
| GL-5 AI / 反馈 | ✅ **主** | 规则判定为主（D-043）；反馈可理解；模式切换不影响判定 |
| GL-6 能力提升 | 轻 | 单课通过即微小能力证据 |
| GL-7 成长可见 | — | 进展呈现主责在闭环 Spec |
| GL-8 下一目标 | — | Back/Next 续课即可，非目标管理 |

> 主战场：**GL-4 + GL-5**。不声称整环八拆。

## Scope

### In Scope

- **固定 NPC 池**（全站 ≤ **4** 个具名角色；可轮换出场，不做好感度）
- **引导链（单课）：** 困境 / 场景 → 心智模型（概念）→ 示例 → 练习（验收题）→ 提交与判定
- **先学后练**信息架构保留（【学】【例】【练】【提交】）；不可去掉讲解只留题
- **concept.story** 任务简报对象字段（mission / scene / npc / npc_line / objective / body / clear_hint…）；与 `concept.normal` 并存
- **概念模式（方案 B）：** 默认偏好只在个人中心改；课内切换临时；**模式不影响题目判定**
- **任务 / 关卡隐喻**与章「幕名」轻钩子（文案层，非经济系统）
- 游客可学；禁止问卷墙

### Out of Scope（须对照 Hard No）

- 联赛 / XP 商店 / 排行榜 / 段位赛 / 宝石货币化  
- **好感度养成**、约会式养成  
- **视觉小说长分叉**、多结局剧情树产品化  
- 跨课大型剧情状态机 / 世界地图（若要做须另开 Arch + Spec）  
- 课平台 / 社区 / 招聘 / IDE / 以代写代码为主价值  
- 真 LLM 作为能跑通前提（D-043：规则判定为主）  
- 削弱 D-039 / D-041 / Hard No「复杂游戏」

## User Flow（禁止 UI）

1. 用户带着当前课进入学习行动  
2. 先接触【学】：正常模式得清晰概念；故事模式得 NPC 困境 + 心智模型叙事（二者知识点一致）  
3. 看【例】对照示范（与练习不同数据/问法）  
4. 做【练】验收题并【提交】，获得可理解判定 / 改进提示  
5. 通过后可续下一课；默认概念模式不因课内临时切换而改变  

```mermaid
flowchart LR
  Enter[进入单课] --> Learn[学: 心智模型]
  Learn --> Example[例: 示范]
  Example --> Practice[练: 验收]
  Practice --> Grade[提交判定]
  Grade --> Next[续下一课或回 Dashboard]
```

## Business Rules

| ID | 规则 | 证据级别 |
|----|------|----------|
| BR-101 | 单课必须先学后练；禁止默认一进来只做题 | Confirmed（D-049） |
| BR-102 | ready 课须有 `concept.normal` 与可用的 `concept.story`（任务简报对象）；示例 ≠ 练习雷同 | Confirmed（D-050/内容约定） |
| BR-103 | 概念模式切换**不得**改变判定结果或答案键 | Confirmed（D-049/051） |
| BR-104 | 默认概念模式仅个人中心写入；课内切换临时（方案 B） | Confirmed（D-051） |
| BR-105 | NPC 池全站 ≤ 4；不做好感度 / 长分叉剧情 | Confirmed（D-056） |
| BR-106 | 禁止联赛 / XP 商店 / 排行等复杂游戏经济冒充坚持 | Confirmed（Hard No + D-056） |
| BR-107 | 反馈以规则判定为主；LLM 非前提；不确定时坦诚边界 | Confirmed（D-043） |

含：Growth Before Monetization、禁止问卷墙、免费可学。

## AI Behavior（若涉及反馈）

| ID | 允许 | 禁止 | 不确定时 |
|----|------|------|----------|
| AI-GL2-01 | 规则判定给出对错与可执行改进点 | 用空洞夸奖 / 假等级代替能力证据 | 坦诚「本课仅规则检查」并引导重读概念或提示 |
| AI-GL2-02 | NPC 台词服务于心智模型 | 代写整项目当主价值；剧情盖过验收 | 回退到 normal 概念陈述 |
| AI-GL2-03 | — | 幻觉权威、编造用户未完成的成就 | 同上 |

## Acceptance Criteria

引用并细化 PRD AC（可测试）；细则以价值闭环表述，禁止 UI 线框。

| AC ID | 准则（价值闭环） | 通过信号 |
|-------|------------------|----------|
| AC-GL2-01 | Given ready 课，When 用户进入，Then 能先获得概念/情境建模再进入验收题（非裸题开场） | 用户能复述本课心智模型要点后再提交 |
| AC-GL2-02 | Given 故事模式可用，When 用户以故事呈现学习，Then 获得 NPC 困境→目标→叙事建模，且知识点与正常模式一致 | 用户能说出「场景里在解决什么概念问题」 |
| AC-GL2-03 | Given 任意概念模式，When 提交同一答案，Then 判定结果一致 | 模式切换前后同答同结果 |
| AC-GL2-04 | Given 用户改默认模式或不改，When 课内临时切换后换课/刷新，Then 按默认模式重新呈现【学】 | 符合方案 B；默认未被课内切换污染 |
| AC-GL2-05 | Given 产品叙事元素存在，When 审查范围，Then 无联赛/XP 商店/排行/好感度/长分叉作为主价值 | Hard No + D-056 边界未被突破 |

对齐 PRD：**AC-05**（US-05）；不削弱 SPEC-GL-001 的 AC-01…04。

## Edge Cases

- 无 story 或 story 不完整：诚实回退 normal，并提示「本课暂无故事稿」；勿空白  
- 游客：可完整学与切换临时模式；默认可 session/cookie 持久，无注册墙  
- 骨架章（未 ready）：不得伪装可玩剧情关卡  
- 示例与练习雷同：视为内容缺陷（须换数据/问法/场景）

## Test Mapping

| Spec / AC | 测试类型（未来） | 备注 |
|-----------|------------------|------|
| AC-GL2-01…02 | 手工走查 / 1～3 人试用（Q-A8） | normal vs story |
| AC-GL2-03…04 | 现有冒烟 + 方案 B 回归 | `test_client` 类 |
| AC-GL2-05 | 文档/产品走查清单 | Hard No 抽检 |
| BR-101…107 | 内容校验脚本 + 手工 | check_content 等 |

本阶段不强制新自动化代码；实现已存在处可回归。

## Open Questions

| ID | 问题 | 状态 |
|----|------|------|
| Q-A8 | 叙事/NPC 是否比教材腔更提升「先建模再练」与回访？ | Open（见 [[Open_Questions]]） |

无阻塞本 Spec Approved 的剩余 OQ（试用为 Continuous Validation）。

## Future Extension

- 跨课连续剧情 / 状态机（须另 Arch）  
- NPC 语音/立绘资源化（非本 Spec）  
- LLM 增强旁白（仍非跑通前提）

## 变更记录

| 日期 | 变更 | 作者 |
|------|------|------|
| 2026-07-23 | 初稿 Approved：NPC 引导式单课契约；对齐 D-056 / US-05 / AC-05 | Execution Agent |
