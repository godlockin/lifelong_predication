-- 命理测算系统数据库表结构
-- Cloudflare D1 (SQLite)

-- 邀请码表
CREATE TABLE IF NOT EXISTS invitation_codes (
    code TEXT PRIMARY KEY,              -- 6位数字邀请码
    created_at TEXT NOT NULL,           -- 创建时间 (ISO 8601)
    used_count INTEGER DEFAULT 0,       -- 使用次数
    last_used_at TEXT,                  -- 最后使用时间
    is_active INTEGER DEFAULT 1,        -- 是否激活 (1=激活, 0=禁用)
    notes TEXT                          -- 备注
);

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_invitation_codes_created 
ON invitation_codes(created_at DESC);

CREATE INDEX IF NOT EXISTS idx_invitation_codes_active 
ON invitation_codes(is_active);

-- 命理计算记录表
CREATE TABLE IF NOT EXISTS fortune_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    invitation_code TEXT NOT NULL,      -- 使用的邀请码
    birth_date TEXT NOT NULL,           -- 出生日期时间
    gender TEXT,                        -- 性别
    city TEXT,                          -- 出生城市
    longitude REAL,                     -- 经度
    timezone INTEGER,                   -- 时区
    bazi_result TEXT,                   -- 八字结果 (JSON)
    ziwei_result TEXT,                  -- 紫微斗数结果 (JSON)
    analysis_result TEXT,               -- 分析结果 (JSON)
    created_at TEXT NOT NULL,           -- 创建时间 (ISO 8601)
    ip_address TEXT,                    -- IP地址（可选）
    user_agent TEXT,                    -- 用户代理（可选）
    FOREIGN KEY (invitation_code) REFERENCES invitation_codes(code)
);

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_fortune_records_invitation 
ON fortune_records(invitation_code);

CREATE INDEX IF NOT EXISTS idx_fortune_records_created 
ON fortune_records(created_at DESC);

CREATE INDEX IF NOT EXISTS idx_fortune_records_birth_date 
ON fortune_records(birth_date);
