-- Python track progress (minimal). Apply after 001_init.sql or via app init.
-- D-058: 中文 COMMENT。规范：docs/05_Architecture/MySQL_Comment_Convention.md

USE leapma;

CREATE TABLE IF NOT EXISTS user_track_progress (
  user_id VARCHAR(36) NOT NULL COMMENT '用户 ID',
  track_id VARCHAR(64) NOT NULL COMMENT '赛道 ID（如 python）',
  chapter_id VARCHAR(64) NOT NULL COMMENT '章节 ID（如 py-01）',
  lesson_id VARCHAR(64) NOT NULL DEFAULT '' COMMENT '课 ID（空串表示章级记录）',
  status VARCHAR(32) NOT NULL DEFAULT 'unlocked' COMMENT '进度状态（如 unlocked 等）',
  last_attempt TEXT NULL COMMENT '最近一次作答原文',
  last_passed TINYINT(1) NOT NULL DEFAULT 0 COMMENT '最近是否通过（0否/1是）',
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后更新时间',
  PRIMARY KEY (user_id, track_id, chapter_id, lesson_id),
  CONSTRAINT fk_utp_user FOREIGN KEY (user_id) REFERENCES users(id)
) ENGINE=InnoDB COMMENT='赛道章节课进度';
