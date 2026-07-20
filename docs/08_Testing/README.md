# 08_Testing

## 职责

定义如何证明 Code 符合 Specification。

在 Source of Truth 链路中，Test 是最后的验证层：

Vision → Product → Specification → Architecture → Code → **Test**

## 包含

- 测试策略
- 质量门禁
- 覆盖率预期（技术栈确定后）
- Bug 分流约定

## 规则

- 验收标准来自 Specification，而非仅来自工单。
- 不稳定测试按缺陷处理。
- 未经过 Architecture / ADR，不在此选定测试框架。

## 相关

跨切面套件放在 `/tests`。单元测试靠近代码。
