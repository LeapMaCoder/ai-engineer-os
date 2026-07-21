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

## 第 1～3 章手工验收（摘要）

1. 首页芯片「学 Python 基础：变量与类型」或「Python 章节目录」  
2. Dashboard 见 15 章；第 4～15 为「未开放」；续学 CTA 的 N/M 正确  
3. 打开第 1～3 章，混合题型 Submit 看规则判定（非真实 LLM）  
4. 全程无问卷墙、游客可学；Run 仍为占位  

示例通过作答：

- py-01-l2：选 **B**  
- py-02-l3：填 `n * n`  
- py-03-l1：选 **B**  

## 原则护栏

禁止问卷墙 · Growth Loop · Hard No · Growth Before Monetization · 不抄袭竞品文本 · 不整份 md 当页面。
