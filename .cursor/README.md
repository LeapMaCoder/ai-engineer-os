# .cursor/

LeapMa 的 Cursor 项目配置。

## 职责

把 AI Native 工程约束编码进规则，使 Agent 默认遵守 SDD。

## 结构

```text
.cursor/
└── rules/
    ├── global/         # 项目级原则
    ├── product/        # 需求与用户价值（禁止过早写代码）
    ├── architecture/   # 设计与 ADR 纪律
    ├── backend/        # 服务实现约束
    ├── frontend/       # 应用实现约束
    ├── ai/             # AI Agent / 导师系统约束
    ├── testing/        # 质量与验证
    └── review/         # 评审门禁与拒绝标准
```

详见 `rules/README.md`。
