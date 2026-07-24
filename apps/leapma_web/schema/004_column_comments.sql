-- D-058: 为已有 leapma 库补全表/列中文 COMMENT（不改类型与约束语义）。
-- 可重复执行：多次 MODIFY 同等定义安全。
-- 规范：docs/05_Architecture/MySQL_Comment_Convention.md
-- Apply: mysql -u... -p leapma < schema/004_column_comments.sql
-- 禁止把密码写进本文件或文档。

USE leapma;

ALTER TABLE users COMMENT = '用户账户（含游客升级后的登录用户）';
ALTER TABLE users
  MODIFY COLUMN id VARCHAR(36) NOT NULL COMMENT '用户主键 UUID',
  MODIFY COLUMN created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  MODIFY COLUMN is_paid TINYINT(1) NOT NULL DEFAULT 0 COMMENT '是否付费用户（0否/1是）';

-- 认证相关列：若尚未存在则跳过（由 003 / app ALTER 先加列）；存在则补 COMMENT
-- 下列语句在列缺失时会失败；app 新装应先跑 init。已有库通常已有这些列。
ALTER TABLE users
  MODIFY COLUMN username VARCHAR(64) NULL COMMENT '登录名（唯一；NULL=未注册/游客体系）',
  MODIFY COLUMN email VARCHAR(255) NULL COMMENT '邮箱（可空）',
  MODIFY COLUMN password_hash VARCHAR(255) NULL COMMENT '密码哈希（可空）',
  MODIFY COLUMN display_name VARCHAR(64) NULL COMMENT '显示昵称（可空）',
  MODIFY COLUMN concept_mode_default VARCHAR(16) NULL COMMENT '默认概念模式（normal|story；NULL=normal）';

ALTER TABLE growth_sessions COMMENT = '首次成长体验会话（SPEC-GL-001）';
ALTER TABLE growth_sessions
  MODIFY COLUMN id VARCHAR(36) NOT NULL COMMENT '会话主键 UUID',
  MODIFY COLUMN user_id VARCHAR(36) NOT NULL COMMENT '所属用户 ID',
  MODIFY COLUMN goal_intent TEXT NULL COMMENT '用户目标意图',
  MODIFY COLUMN position_hint TEXT NULL COMMENT '轻量能力位置感/推断摘要',
  MODIFY COLUMN probe_question TEXT NULL COMMENT '可选探针题干',
  MODIFY COLUMN probe_answer TEXT NULL COMMENT '探针对答',
  MODIFY COLUMN next_step TEXT NULL COMMENT '个性化下一步行动',
  MODIFY COLUMN exercise_prompt TEXT NULL COMMENT '本轮练习题干',
  MODIFY COLUMN attempt_text TEXT NULL COMMENT '用户作答原文',
  MODIFY COLUMN feedback_body TEXT NULL COMMENT '反馈正文',
  MODIFY COLUMN feedback_uncertain TINYINT(1) NOT NULL DEFAULT 0 COMMENT '反馈是否标为不确定（0否/1是）',
  MODIFY COLUMN feedback_rejected_codegen TINYINT(1) NOT NULL DEFAULT 0 COMMENT '是否拒绝代写整项目请求（0否/1是）',
  MODIFY COLUMN progress_note TEXT NULL COMMENT '进展备注（相对目标）',
  MODIFY COLUMN next_intent TEXT NULL COMMENT '下一意图/续环方向',
  MODIFY COLUMN stage VARCHAR(32) NOT NULL DEFAULT 'orient' COMMENT '会话阶段（如 orient 等）',
  MODIFY COLUMN created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  MODIFY COLUMN updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后更新时间';

ALTER TABLE user_track_progress COMMENT = '赛道章节课进度';
ALTER TABLE user_track_progress
  MODIFY COLUMN user_id VARCHAR(36) NOT NULL COMMENT '用户 ID',
  MODIFY COLUMN track_id VARCHAR(64) NOT NULL COMMENT '赛道 ID（如 python）',
  MODIFY COLUMN chapter_id VARCHAR(64) NOT NULL COMMENT '章节 ID（如 py-01）',
  MODIFY COLUMN lesson_id VARCHAR(64) NOT NULL DEFAULT '' COMMENT '课 ID（空串表示章级记录）',
  MODIFY COLUMN status VARCHAR(32) NOT NULL DEFAULT 'unlocked' COMMENT '进度状态（如 unlocked 等）',
  MODIFY COLUMN last_attempt TEXT NULL COMMENT '最近一次作答原文',
  MODIFY COLUMN last_passed TINYINT(1) NOT NULL DEFAULT 0 COMMENT '最近是否通过（0否/1是）',
  MODIFY COLUMN updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后更新时间';
