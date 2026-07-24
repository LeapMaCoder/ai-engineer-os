---
title: 当前状态
type: project
status: active
owner: ""
created: 2026-07-20
updated: 2026-07-21
tags:
  - project
  - state
  - leapma
---

# Current State — 当前状态

快照：`2026-07-23`

## 1. 产品状态

| 项 | 状态 |
|----|------|
| 初期赛道 | **Python**（D-042） |
| 章节 | py-01～03 **ready**；py-04～15 skeleton（D-044/047） |
| 课内教学 | 先学后练 + **跃迁站四 NPC**（D-057）；契约 SPEC-GL-002 / D-056 |
| MySQL | 全表全字段中文 COMMENT（D-058） |
| 反馈 | 规则判定优先；LLM Later（D-043） |
| 代码 | `apps/leapma_web` + `content/python/` |
| 主存 | MySQL `leapma`（凭据仅在本地 `.env`） |

## 2. 变更日志

| 日期 | 变化 |
|------|------|
| 2026-07-23 | **D-057 / D-058**：锁定跃迁站四 NPC 并收口前三章故事；MySQL 全字段中文 COMMENT 规范与迁移；**未 commit** |
| 2026-07-23 | **D-056 文档债**：Decision/Open Q-A8 / SPEC-GL-002 Approved / US-05·AC-05 / Vision·Principles 叙事型坚持对齐；**仅文档，未改 apps；未 commit** |
| 2026-07-23 | **D-055**：整体 UI 微调（间距/课内分区/移动端）；保持 D-048 令牌；**未 commit** |
| 2026-07-23 | **D-054**：打磨 `/profile` 账户与设置分区；Dashboard 强化「接下来练什么」；**未 commit** |
| 2026-07-23 | **D-053**：打磨 Python 第 1～3 章（讲解/故事/示例≠练习/判定收紧）；不开新章；**未 commit** |
| 2026-07-22 | **D-052**：个人中心 `/profile` 独立；Dashboard 仅续学摘要联动；方案 B 默认模式写入点迁到 profile；**未 commit** |
| 2026-07-22 | **D-051 方案 B**：`concept_mode_default` 默认偏好 + 课内临时切换；刷新/换课回默认；**未 commit** |
| 2026-07-22 | **D-050**：`concept.story` 升为任务简报对象 + `story-mission` UI 壳；第 1～3 章 ready 课改写；旧字符串兼容；**未 commit** |
| 2026-07-22 | **内容补全**：第 1～3 章全部 ready 课补齐 `concept.story` + `example`（示例≠练习）；README/D-049 同步 story 必填；**未 commit** |
| 2026-07-21 | **D-049**：课内先学后练 + `concept.normal`/`story` 钩子；第 1～3 章 ready 课已补讲解；**未 commit** |
| 2026-07-21 | **D-048**：全站暗色终端风（design tokens）；无复杂游戏经济 UI；**未 commit** |
| 2026-07-21 | **Multitask C**：Dashboard 对齐 Boot.dev IA + 轻量登录注册；**未 commit** |
| 2026-07-21 | **D-045**：视觉重做 + 游客 Dashboard Demo；**未 commit** |
| 2026-07-21 | D-042/043/044；Python 第 1 章可玩 + MySQL；**未 commit** |
