-- SPEC-GL-001 First Growth Experience — minimal MySQL schema
-- D-058: 所有表/字段须中文 COMMENT。规范：docs/05_Architecture/MySQL_Comment_Convention.md
-- Apply: mysql -u... -p < schema/001_init.sql

CREATE DATABASE IF NOT EXISTS leapma CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE leapma;

CREATE TABLE IF NOT EXISTS users (
  id VARCHAR(36) PRIMARY KEY COMMENT '用户主键 UUID',
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  is_paid TINYINT(1) NOT NULL DEFAULT 0 COMMENT '是否付费用户（0否/1是）'
) ENGINE=InnoDB COMMENT='用户账户（含游客升级后的登录用户）';

CREATE TABLE IF NOT EXISTS growth_sessions (
  id VARCHAR(36) PRIMARY KEY COMMENT '会话主键 UUID',
  user_id VARCHAR(36) NOT NULL COMMENT '所属用户 ID',
  goal_intent TEXT NULL COMMENT '用户目标意图',
  position_hint TEXT NULL COMMENT '轻量能力位置感/推断摘要',
  probe_question TEXT NULL COMMENT '可选探针题干',
  probe_answer TEXT NULL COMMENT '探针对答',
  next_step TEXT NULL COMMENT '个性化下一步行动',
  exercise_prompt TEXT NULL COMMENT '本轮练习题干',
  attempt_text TEXT NULL COMMENT '用户作答原文',
  feedback_body TEXT NULL COMMENT '反馈正文',
  feedback_uncertain TINYINT(1) NOT NULL DEFAULT 0 COMMENT '反馈是否标为不确定（0否/1是）',
  feedback_rejected_codegen TINYINT(1) NOT NULL DEFAULT 0 COMMENT '是否拒绝代写整项目请求（0否/1是）',
  progress_note TEXT NULL COMMENT '进展备注（相对目标）',
  next_intent TEXT NULL COMMENT '下一意图/续环方向',
  stage VARCHAR(32) NOT NULL DEFAULT 'orient' COMMENT '会话阶段（如 orient 等）',
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后更新时间',
  CONSTRAINT fk_gs_user FOREIGN KEY (user_id) REFERENCES users(id)
) ENGINE=InnoDB COMMENT='首次成长体验会话（SPEC-GL-001）';
