# apps/

面向用户的应用放在此目录。

## 职责

- 承载可独立交付的客户端（如 Web，以及未来的移动端）。
- 将 UI / 运行时关注点与 `services/`、`packages/` 分离。

## 规则

- **在**对应应用的 Specification + Architecture 完成前，**不要**添加应用代码。
- 每个应用应有自己的 `README.md`，说明范围与归属。
- 共享逻辑放入 `packages/`，禁止在多个 app 间复制粘贴。

## 状态

Phase 0 占位。尚未创建任何应用。
