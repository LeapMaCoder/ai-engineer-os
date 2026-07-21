# LeapMa Web — First Growth Experience + Python 赛道

Python **Flask + Jinja SSR**。初期赛道：**Python**（D-042 / D-047）。反馈：**规则判定**为主（D-043）。视觉：**暗色终端风**（D-048 · `design_system.json`）。

## 进度

| 章 | 状态 |
|----|------|
| 第 1 章 变量与类型 | **可玩**（5 练 · mcq/fill/short/code） |
| 第 2 章 函数 | **可玩**（5 练） |
| 第 3 章 作用域 | **可玩**（5 练） |
| 第 4～15 章 | 骨架 · Dashboard 显示「未开放」 |

题源：Founder Engineer OS Obsidian 笔记**改编**（非竞品官网原文）。详见 `docs/03_Product/MVP/Python_Track_Outline.md`。

## 入口 URL

| 页面 | URL |
|------|-----|
| 首页 | http://127.0.0.1:5000/ |
| 游客 Dashboard | http://127.0.0.1:5000/dashboard （或 `/me`） |
| Python 章节 | http://127.0.0.1:5000/track/python |

顶栏：品牌回首页 · Dashboard · 开始练。

## 本地 MySQL（推荐）

1. 确保 MySQL 可连；库名建议 `leapma`（应用可自动建库建表）。  
2. 在**被 gitignore 的**仓库根或本目录 `.env` 配置（**勿把真实密码写进 README/代码**）：

```env
DATABASE_URL=mysql://USER:PASSWORD@127.0.0.1:3306/leapma
LEAPMA_LLM_PROVIDER=mock
FLASK_SECRET_KEY=dev-change-me
```

也可手工执行：`schema/001_init.sql`、`schema/002_track_progress.sql`。

## 启动

```powershell
cd apps/leapma_web
uv venv
uv pip install -e .
uv run flask --app wsgi run --debug --port 5000
```

打开 http://127.0.0.1:5000/

## 冒烟（Flask test client）

```powershell
cd apps/leapma_web
uv run python test_client.py
```

会对第 1～3 章各提交一题并断言判定通过。

## 课内结构（先学后练）

每课页固定分区：**【学】→【例】→【练】→【提交】**。默认先展示讲解；可用「去练习」锚点跳到题目，但不可去掉概念区。

概念区支持模式切换：`正常模式 | 故事模式`（仅切换文案，不影响判定）。无 `concept.story` 时故事按钮灰掉。

### Lesson JSON 钩子（`content/python/chapter_XX.json`）

| 字段 | 必填 | 说明 |
|------|------|------|
| `concept.normal` | 是 | 正常模式讲解 |
| `concept.story` | 否 | 故事模式；缺省则 UI 不启用 |
| `example.code` / `example.note` | 建议有 | 示例代码与说明 |
| `type` / `prompt` / … | 是 | 练与判定（亦可放进 `exercises[0]`，loader 会提升） |

旧字段（`coach`、`prompt`、`checks`…）仍兼容；无 `concept` 时 loader 用 `coach` 作薄回退。

示范含 story：`py-01-l2`、`py-02-l1`。

## 第 1～3 章手工验收（摘要）

1. 首页芯片「学 Python 基础：变量与类型」或「Python 章节目录」  
2. Dashboard 见 15 章；第 4～15 为「未开放」；续学 CTA 的 N/M 正确  
3. 打开任意 ready 课：先见【学】【例】，再【练】【提交】；含 story 的课可切换模式  
4. 混合题型 Submit 看规则判定（非真实 LLM）  
5. 全程无问卷墙、游客可学；Run 仍为占位；无 XP/联赛 UI  

示例通过作答：

- py-01-l2：选 **B**  
- py-02-l3：填 `n * n`  
- py-03-l1：选 **B**  

## 原则护栏

禁止问卷墙 · Growth Loop · Hard No · Growth Before Monetization · 不抄袭竞品文本 · 不整份 md 当页面。
