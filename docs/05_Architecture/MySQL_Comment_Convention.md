---
title: MySQL Comment Convention
type: architecture
status: active
created: 2026-07-23
updated: 2026-07-23
tags:
  - architecture
  - mysql
  - leapma
---

# MySQL 注释规范（D-058）

> **主真源：** 本文。交叉引用见文末。  
> **适用范围：** LeapMa **MySQL 主存**（ADR-0002）。SQLite 无 COMMENT 能力，本地 fallback **不强求** COMMENT。

## 1. 强制规则

1. **所有表、所有字段必须有中文 COMMENT**（表职责 + 列业务含义）。  
2. 新建 / 变更 DDL 时**同步写 COMMENT**，禁止「先建表后补注释」成为常态。  
3. **真源文件：** `apps/leapma_web/schema/*.sql`。  
4. **运行时 DDL：** `leapma_web/db.py` 中 `_MYSQL_DDL` 与 `_ensure_*` 的 ALTER 必须带**同等**中文 COMMENT，保证新装库一致。  
5. **已有库：** 用可重复执行的 `ALTER TABLE ... COMMENT='...'` / `MODIFY COLUMN ... COMMENT '...'` 迁移补全（如 `schema/004_column_comments.sql`）；勿只改文件不改库。  
6. 为写 COMMENT 而 `MODIFY` 时：**不得改变列类型、NULL、默认值、约束语义**（仅补注释）。

## 2. 写法要求

| 对象 | 要求 |
|------|------|
| 表 COMMENT | 一句话说明表职责（中文） |
| 列 COMMENT | 业务含义；枚举写清取值；NULL 语义写清（中文、简洁） |

示例：

```sql
CREATE TABLE users (
  id VARCHAR(36) PRIMARY KEY COMMENT '用户主键 UUID',
  concept_mode_default VARCHAR(16) NULL COMMENT '默认概念模式（normal|story；NULL=normal）'
) ENGINE=InnoDB COMMENT='用户账户（含游客升级后的登录用户）';
```

## 3. 与 SQLite

- 规范**针对 MySQL 主存**。  
- SQLite DDL（`_SQLITE_DDL`）可不写 COMMENT；行为契约仍以 MySQL schema 为准。

## 4. 交叉引用

- Decision_Log：**D-058**  
- [[ADR-0002_Primary_Store_for_SPEC-GL-001]]（MySQL 主存）  
- [[Development_Environment]]（环境能力；注释规范以本文为准）  
- `apps/leapma_web/README.md` · `apps/leapma_web/schema/`
