# LeapMa Web — First Growth Experience + Python 赛道

Python **Flask + Jinja SSR**。初期赛道：**Python**（D-042）。反馈：**规则判定**为主（D-043）。章节路径：D-044。

## 进度

| 章 | 状态 |
|----|------|
| 第 1 章 print 与字符串 | **可玩**（3 练） |
| 第 2 章 变量 | 骨架 |
| 第 3 章 if | 骨架 |

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

## 第 1 章手工验收

1. 首页点芯片「学 Python 基础：会用 print」或进「Python 章节目录」  
2. 打开 **第 1 章** → 依次三练，提交代码，看**判定对错**（非真实 LLM）  
3. 第 3 练通过后进入进展页，写具体进展 + 再来方向（AC-03）  
4. 确认全程无问卷墙、未付费可完成  

示例通过作答（原创练习，自行输入）：

- 练 1：`print("Hello LeapMa")`  
- 练 2：`print("I write Python")`  
- 练 3：两行 `print("Go")` 与 `print("Learn")`  

## 原则护栏

禁止问卷墙 · Growth Loop · Hard No · Growth Before Monetization · 不抄袭竞品文本。
