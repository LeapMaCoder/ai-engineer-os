# LeapMa

AI Native 程序员成长平台。

LeapMa **不是**传统课程平台，而是帮助程序员持续成长的产品，核心能力包括：

- AI 导师
- 动态学习路径
- 知识图谱
- 游戏化成长系统

## 从这里开始

| 角色 | 入口 |
|------|------|
| 任何人 / AI Agent | **[项目仪表盘](docs/00_Project/Project_Dashboard.md)** |
| 找文档 | **[文档索引](docs/INDEX.md)** |
| 看阶段 | [路线图](docs/00_Project/Roadmap.md) |
| 看未决 | [未决问题](docs/00_Project/Open_Questions.md) |

## 当前阶段

**Phase 5 — Python 15 章骨架**（第 1～3 章可玩；4～15 skeleton；规则反馈）

详情：[leapma_web README](apps/leapma_web/README.md) · [Python_Track_Outline](docs/03_Product/MVP/Python_Track_Outline.md)

**Agent 不 commit。**

## 开发方式

LeapMa 采用 **Specification Driven Development（SDD）**。

```text
Vision → Product → Specification → Architecture → Code → Test
```

流程见 [Development_Workflow](docs/08_Development/Development_Workflow.md)。

## 仓库目录

产品名 LeapMa；本仓库目录 / GitHub 名为 `ai-engineer-os`。

```text
ai-engineer-os/
├── docs/
│   ├── 00_Project/      # 导航与状态（先读 Dashboard）
│   ├── 01_Vision/
│   ├── 02_Research/
│   ├── 03_Product/
│   ├── INDEX.md         # 文档索引
│   └── ...
├── apps/ services/ packages/ infrastructure/ tests/ scripts/
├── .cursor/             # AI Rules（含文档导航同步）
├── README.md
└── CHANGELOG.md
```

完整关系图：[Project_Map](docs/00_Project/Project_Map.md)

## 协作约定

1. 不要从写代码开始。
2. 先读 Dashboard，再改文档。
3. 重要文档变更同步 Dashboard + Map + INDEX。
4. 使用 `docs/templates/`。
5. 重要技术决策写 ADR（Phase 2+）。

## License

待定
