-- Python track progress (minimal). Apply after 001_init.sql or via app init.

USE leapma;

CREATE TABLE IF NOT EXISTS user_track_progress (
  user_id VARCHAR(36) NOT NULL,
  track_id VARCHAR(64) NOT NULL,
  chapter_id VARCHAR(64) NOT NULL,
  lesson_id VARCHAR(64) NOT NULL DEFAULT '',
  status VARCHAR(32) NOT NULL DEFAULT 'unlocked',
  last_attempt TEXT NULL,
  last_passed TINYINT(1) NOT NULL DEFAULT 0,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (user_id, track_id, chapter_id, lesson_id),
  CONSTRAINT fk_utp_user FOREIGN KEY (user_id) REFERENCES users(id)
) ENGINE=InnoDB;
