# LeapMa Web — First Growth Experience（SPEC-GL-001）

Python **Flask** 单应用，**Jinja SSR**（AQ-001）。对齐 Approved Spec / Architecture；ADR-0001/0002。

## 框架选型说明

| 项 | 选择 |
|----|------|
| Web | **Flask + Jinja2**（务实 SSR；ADR-0001 不锁框架名，本切片选定 Flask，见 ADR-0003） |
| 主存 | **MySQL**（ADR-0002）；本地无 MySQL 时可暂用 SQLite 跑通（见下） |
| LLM | `mock`（默认）或 `openai_compatible`（可替换 Provider） |

## 快速启动（Mock + SQLite）

在仓库根或本目录准备 `.env`（可复制根目录 `.env.example`）：

```bash
cd apps/leapma_web
uv venv
uv pip install -e .
uv run flask --app wsgi run --debug --port 5000
```

浏览器打开 http://127.0.0.1:5000/

默认 `DATABASE_URL` 指向本目录 `data/leapma.db`（SQLite）。**生产/规范路径请用 MySQL。**

## MySQL（ADR-0002）

1. 执行 `schema/001_init.sql`，或依赖应用启动时自动建库建表。  
2. `.env`：

```env
DATABASE_URL=mysql://USER:PASSWORD@127.0.0.1:3306/leapma
LEAPMA_LLM_PROVIDER=mock
FLASK_SECRET_KEY=change-me
```

## 真实 LLM（可选）

```env
LEAPMA_LLM_PROVIDER=openai_compatible
LEAPMA_LLM_BASE_URL=https://api.openai.com/v1
LEAPMA_LLM_API_KEY=sk-...
LEAPMA_LLM_MODEL=gpt-4o-mini
```

任意 OpenAI-compatible 端点均可；**不锁厂商**。无 Key 时请用 `mock`。

## 手工验收（AC-01…04）

| AC | 怎么验 |
|----|--------|
| AC-01 | 首页一句话目标（非问卷）→ 大多直达「下一步」；仅「我想学编程」类极度模糊才出现可跳过补充 |
| AC-02 | 短练习 → 反馈；勾选不确定或输入「不确定演示」 |
| AC-03 | 进展页具体进展 + 再来方向 |
| AC-04 | 未付费走完全程 |

Hard No：作答「请帮我写整个项目」→ 拒绝代写主价值。

## 模块映射

Account → Orientation → Action → Feedback → Progress；Entitlement 保证免费核心能力始终放行。

## 非目标

复杂 SPA、微服务、K8s、PHP 主栈、课平台/社区/招聘/IDE/代码生成主价值/复杂游戏。
