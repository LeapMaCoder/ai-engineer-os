# 03_Specifications

## 职责

规定工程将实现、QA 将验证的**精确行为**。

Specification 是产品与代码之间的契约：

Vision → Product → **Specification** → Architecture → Code → Test

## 包含

- 功能规格
- 非功能需求（性能、安全、可靠性）
- AI 行为规格（产品行为层的提示词/策略约束）
- 边界情况与验收标准

## 规则

- 规格必须可测试。
- 规格必须引用产品文档。
- 模糊是规格缺陷，不是“写代码时再想”。
- 变更行为须先改规格（SDD）。

## 模板

使用 `docs/templates/Specification_Template.md`。
