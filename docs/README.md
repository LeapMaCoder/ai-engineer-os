# docs/ — LeapMa Source of Truth

`docs/` 是 LeapMa 的**唯一权威来源（Source of Truth）**。

代码不定义产品意图，文档才定义。

## 先读这里

1. [[Project_Dashboard]] — 项目当前状态总览  
2. [[docs/INDEX]] — 全文档索引  
3. [[Project_Map]] — 目录与文档关系  

## 权威链路

```text
Vision（愿景）
  → Product（产品）
    → Specification（规格）
      → Architecture（架构）
        → Code（代码）
          → Test（测试）
```

| 层级 | 含义 | 目录 |
|------|------|------|
| Vision | 为什么做 LeapMa；长期北极星 | `01_Vision/` |
| Product | 服务谁；问题与结果 | `03_Product/`（由 `02_Research/` 支撑） |
| Specification | 要构建与验证的精确行为 | `04_Specifications/` |
| Architecture | 系统如何实现规格 | `05_Architecture/` + `06_ADR/` |
| Code | 已批准规格/架构的实现 | `apps/`、`services/`、`packages/` |
| Test | 证明代码符合规格 | `tests/` + `09_Testing/` |

治理层 `00_Project/` 不替代上述链路，只负责**状态可见与导航**。

### 不可协商规则

1. **没有**对应的产品定义与 Specification，**禁止**写功能代码。
2. **没有**更新 Architecture 文档，**禁止**改架构；重大决策必须 ADR。
3. **测试断言的是 Specification**，不是实现者的临时想法。
4. 代码与文档冲突时，**以文档为准**，直到按 SDD 流程有意修订。
5. Research 支撑 Product；Research 本身**不授权**实现。
6. 重要文档变更必须同步 Dashboard / Map / INDEX。

## 目录地图

| 文件夹 | 职责 |
|--------|------|
| `00_Project` | 项目导航、阶段、状态、未决问题 |
| `01_Vision` | 使命、原则、北极星结果 |
| `02_Research` | 市场、竞品、用户、访谈 |
| `03_Product` | ICP、PRD、画像、旅程、成功指标 |
| `04_Specifications` | 功能 / 非功能 / AI 行为规格 |
| `05_Architecture` | 系统设计、边界、数据与 AI 设计 |
| `06_ADR` | 架构决策记录 |
| `07_Sprint` | Sprint 目标、计划、纪要 |
| `08_Development` | 流程、AI 角色、工程实践 |
| `09_Testing` | 测试策略、计划、质量门禁 |
| `10_Release` | 发布说明、清单、放量 |
| `11_Operations` | Runbook、监控、事故流程 |
| `Archive` | 已废止文档（保留历史，勿随意删除） |
| `templates/` | 适配 Obsidian 的 SDD 模板 |
| `INDEX.md` | 全库索引 |

## 如何新增工作

1. 从 `templates/` 复制模板。
2. 放到对应编号目录。
3. 链接上游文档（Vision → Product → Spec → Architecture）。
4. 同步 [[Project_Dashboard]] / [[Project_Map]] / [[docs/INDEX]]。
5. 然后才可以开实现任务（需门禁满足）。
