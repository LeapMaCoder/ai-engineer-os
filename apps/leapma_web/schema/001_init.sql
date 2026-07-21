-- SPEC-GL-001 First Growth Experience — minimal MySQL schema
-- Apply: mysql -u... -p < schema/001_init.sql

CREATE DATABASE IF NOT EXISTS leapma CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE leapma;

CREATE TABLE IF NOT EXISTS users (
  id VARCHAR(36) PRIMARY KEY,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  is_paid TINYINT(1) NOT NULL DEFAULT 0
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS growth_sessions (
  id VARCHAR(36) PRIMARY KEY,
  user_id VARCHAR(36) NOT NULL,
  goal_intent TEXT NULL,
  position_hint TEXT NULL,
  probe_question TEXT NULL,
  probe_answer TEXT NULL,
  next_step TEXT NULL,
  exercise_prompt TEXT NULL,
  attempt_text TEXT NULL,
  feedback_body TEXT NULL,
  feedback_uncertain TINYINT(1) NOT NULL DEFAULT 0,
  feedback_rejected_codegen TINYINT(1) NOT NULL DEFAULT 0,
  progress_note TEXT NULL,
  next_intent TEXT NULL,
  stage VARCHAR(32) NOT NULL DEFAULT 'orient',
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT fk_gs_user FOREIGN KEY (user_id) REFERENCES users(id)
) ENGINE=InnoDB;
