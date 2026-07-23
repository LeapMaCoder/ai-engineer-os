-- Plan B: default concept mode preference on users (MySQL).
-- App also auto-ALTERs via _ensure_auth_columns(); this file is for manual ops.
-- Apply: mysql -u... -p leapma < schema/003_concept_mode_default.sql

USE leapma;

ALTER TABLE users
  ADD COLUMN concept_mode_default VARCHAR(16) NULL
  COMMENT 'normal|story; NULL = normal';
