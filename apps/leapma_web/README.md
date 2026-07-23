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
| Dashboard（续学） | http://127.0.0.1:5000/dashboard |
| 个人中心 | http://127.0.0.1:5000/profile （`/me` → 302） |
| Python 章节 | http://127.0.0.1:5000/track/python |

顶栏：品牌回首页 · Dashboard · 个人中心 · 开始练。

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

概念区支持模式切换：`正常模式 | 故事模式`（**切换 UI 壳与文案**，不影响判定）。**方案 B**：个人中心（`/profile`）设「默认概念模式」；每次打开/刷新课按默认渲染；课内切换仅本课临时、不写回默认、不写 URL。故事模式开启时：【学】变为 `story-mission` 任务简报面板；【例】/【练】标题可显示为「任务示范」/「关卡验收」。第 1～3 章 ready 课均含完整 `concept.story` 对象；缺 story 的旧课仍会灰掉（兼容）；若默认是故事但本课无稿，回退正常并提示。

Dashboard 仅展示续学与章列表，个人信息为摘要行（昵称 · 默认模式 → 管理）；完整资料表单只在个人中心。

### Lesson JSON 钩子（`content/python/chapter_XX.json`）

| 字段 | 必填 | 说明 |
|------|------|------|
| `concept.normal` | 是 | 正常模式讲解 |
| `concept.story` | 是（ready 课） | **任务简报对象**（见下）；旧字符串会被 loader 包成 `{ body }` 并补默认字段 |
| `example.code` / `example.note` | 是（ready 课） | 示范代码与一句话说明；**不得与练习同段代码/同问法** |
| `type` / `prompt` / … | 是 | 练与判定（亦可放进 `exercises[0]`，loader 会提升） |

#### `concept.story` 对象（故事模式）

```json
"story": {
  "mission_title": "仓库夜巡：认清贴签",
  "scene": "冷链仓库 A3 货架",
  "npc": "仓管阿哲",
  "npc_line": "别把等号当成数学题。这里是贴签作业。",
  "objective": "选出 score = 100 时等号的最准确含义。",
  "body": "叙事正文……",
  "clear_hint": "可选：通关提示"
}
```

ready 课至少齐全：`mission_title` / `scene` / `npc` / `npc_line` / `objective` / `body`。无 XP / 商店 / 排行。

旧字段（`coach`、`prompt`、`checks`…）仍兼容；无 `concept` 时 loader 用 `coach` 作薄回退。

快速校验：`uv run python check_content.py`（断言每课有 story 任务对象 + example，且 example.code 不与 prompt 完全相同）。

## 第 1～3 章手工验收（摘要）

1. 首页芯片「学 Python 基础：变量与类型」或「Python 章节目录」  
2. Dashboard 见 15 章；第 4～15 为「未开放」；续学 CTA 的 N/M 正确；个人信息仅摘要链到 `/profile`  
2b. `/profile` 可改昵称与默认概念模式；游客可见首次进入时间；无强制注册  
3. 打开任意 ready 课：先见【学】【例】，再【练】【提交】；切故事模式应见 `story-mission` 任务简报（金/绿任务条）  

4. 混合题型 Submit 看规则判定（非真实 LLM）  
5. 全程无问卷墙、游客可学；Run 仍为占位；无 XP/联赛 UI  

示例通过作答：

- py-01-l2：选 **B**  
- py-02-l3：填 `n * n`  
- py-03-l1：选 **B**  

## 原则护栏

禁止问卷墙 · Growth Loop · Hard No · Growth Before Monetization · 不抄袭竞品文本 · 不整份 md 当页面。
