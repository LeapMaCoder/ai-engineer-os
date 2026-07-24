-- Plan B: default concept mode preference on users (MySQL).
-- D-058: 中文 COMMENT。App 亦经 _ensure_auth_columns 自动 ALTER。
-- Apply: mysql -u... -p leapma < schema/003_concept_mode_default.sql

USE leapma;

-- 若列已存在会报错；新装请依赖 001/004 或 app init。已有库且无此列时执行：
ALTER TABLE users
  ADD COLUMN concept_mode_default VARCHAR(16) NULL
  COMMENT '默认概念模式（normal|story；NULL=normal）';
