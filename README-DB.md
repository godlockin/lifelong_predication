# 数据库配置和使用指南

## 概述

本项目使用 **Cloudflare D1**（基于SQLite的边缘数据库）来存储邀请码和用户的命理计算记录。

## 数据库架构

### 表结构

#### `invitation_codes` - 邀请码表

| 字段 | 类型 | 说明 |
|------|------|------|
| code | TEXT (主键) | 6位数字邀请码 |
| created_at | TEXT | 创建时间 (ISO 8601) |
| used_count | INTEGER | 使用次数 |
| last_used_at | TEXT | 最后使用时间 |
| is_active | INTEGER | 是否激活 (1=激活, 0=禁用) |
| notes | TEXT | 备注 |

#### `fortune_records` - 命理计算记录表

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER (主键) | 记录ID |
| invitation_code | TEXT | 使用的邀请码 |
| birth_date | TEXT | 出生日期时间 |
| gender | TEXT | 性别 |
| city | TEXT | 出生城市 |
| longitude | REAL | 经度 |
| timezone | INTEGER | 时区 |
| bazi_result | TEXT | 八字结果 (JSON) |
| ziwei_result | TEXT | 紫微斗数结果 (JSON) |
| analysis_result | TEXT | 分析结果 (JSON) |
| created_at | TEXT | 创建时间 |
| ip_address | TEXT | IP地址 |
| user_agent | TEXT | 用户代理 |

## 初始化步骤

### 1. 创建 D1 数据库

```bash
wrangler d1 create life-fortune-db
```

该命令会返回数据库信息，包含 `database_id`。

### 2. 更新 wrangler.toml

将返回的 `database_id` 填入 `wrangler.toml` 文件的 D1 配置部分：

```toml
[[d1_databases]]
binding = "DB"
database_name = "life-fortune-db"
database_id = "YOUR_DATABASE_ID_HERE"  # 填写这里
```

### 3. 运行初始化脚本

```bash
./db-init.sh
```

该脚本会：
- 引导您完成数据库创建流程
- 应用数据库架构（本地和远程）
- 可选：创建测试邀请码

### 4. 配置管理员密码

**本地开发环境：**

在 `.dev.vars` 文件中添加：
```
ADMIN_PASSWORD=your_admin_password
```

**生产环境：**

```bash
wrangler secret put ADMIN_PASSWORD
```

## 数据库操作命令

### 本地数据库操作

```bash
# 执行 SQL 文件
wrangler d1 execute life-fortune-db --local --file=./schema.sql

# 执行 SQL 命令
wrangler d1 execute life-fortune-db --local --command="SELECT * FROM invitation_codes;"

# 查看所有邀请码
wrangler d1 execute life-fortune-db --local --command="SELECT code, created_at, used_count, is_active FROM invitation_codes ORDER BY created_at DESC;"

# 查看用户记录统计
wrangler d1 execute life-fortune-db --local --command="SELECT COUNT(*) as total, invitation_code FROM fortune_records GROUP BY invitation_code;"
```

### 生产数据库操作

将 `--local` 替换为 `--remote` 即可操作生产数据库：

```bash
wrangler d1 execute life-fortune-db --remote --file=./schema.sql
```

### 常用查询

```sql
-- 查看所有邀请码及使用情况
SELECT code, created_at, used_count, last_used_at, is_active, notes 
FROM invitation_codes 
ORDER BY created_at DESC;

-- 查看最近的用户提交
SELECT id, invitation_code, birth_date, gender, city, created_at 
FROM fortune_records 
ORDER BY created_at DESC 
LIMIT 10;

-- 统计每个邀请码的使用次数
SELECT invitation_code, COUNT(*) as submit_count 
FROM fortune_records 
GROUP BY invitation_code 
ORDER BY submit_count DESC;

-- 手动插入邀请码
INSERT INTO invitation_codes (code, created_at, notes) 
VALUES ('123456', datetime('now'), '特殊邀请码');

-- 禁用邀请码
UPDATE invitation_codes SET is_active = 0 WHERE code = '123456';

-- 启用邀请码
UPDATE invitation_codes SET is_active = 1 WHERE code = '123456';
```

## API 端点

### 公开端点

#### 验证邀请码
```bash
POST /verify-code
Content-Type: application/json

{
  "code": "123456"
}
```

#### 提交命理计算
```bash
POST /submit
Content-Type: application/json

{
  "invitationCode": "123456",
  "birthDate": "2001-05-20T13:30:00",
  "gender": "男",
  "city": "北京"
}
```

### 管理员端点（需要认证）

所有管理员端点都需要在请求头中添加：
```
X-Admin-Password: your_admin_password
```

#### 生成邀请码
```bash
POST /admin/invitation-codes
X-Admin-Password: your_admin_password
Content-Type: application/json

{
  "count": 5,
  "notes": "批量生成"
}
```

#### 获取邀请码列表
```bash
GET /admin/invitation-codes?limit=20&offset=0
X-Admin-Password: your_admin_password
```

#### 禁用/启用邀请码
```bash
PATCH /admin/invitation-codes/123456
X-Admin-Password: your_admin_password
Content-Type: application/json

{
  "active": false
}
```

#### 获取用户记录
```bash
GET /admin/records?limit=20&offset=0
X-Admin-Password: your_admin_password
```

#### 获取记录详情
```bash
GET /admin/records/1
X-Admin-Password: your_admin_password
```

## 管理员后台

访问 `http://localhost:8787/admin.html`（本地）或 `https://your-domain.workers.dev/admin.html`（生产）

功能：
- 🔐 密码登录
- ➕ 批量生成邀请码
- 📋 查看邀请码列表和使用情况
- 👥 查看用户提交记录
- 🔍 查看用户记录详情

## 本地开发

```bash
# 启动本地开发服务器
npm run dev

# 访问管理员后台
open http://localhost:8787/admin.html

# 测试 API
curl http://localhost:8787/verify-code \
  -H "Content-Type: application/json" \
  -d '{"code": "123456"}'
```

## 生产部署

```bash
# 确保已设置管理员密码
wrangler secret put ADMIN_PASSWORD

# 确保已设置 Gemini API Key
wrangler secret put GEMINI_API_KEY

# 部署
npm run deploy
```

## 数据备份

### 导出数据

```bash
# 导出邀请码
wrangler d1 execute life-fortune-db --remote --command="SELECT * FROM invitation_codes;" --json > backup_codes.json

# 导出用户记录（不含详细结果）
wrangler d1 execute life-fortune-db --remote --command="SELECT id, invitation_code, birth_date, gender, city, created_at FROM fortune_records;" --json > backup_records.json
```

### 数据库迁移

如需迁移到新数据库：

1. 创建新数据库：`wrangler d1 create life-fortune-db-new`
2. 应用架构：`wrangler d1 execute life-fortune-db-new --remote --file=./schema.sql`
3. 导出旧数据并导入新数据库

## 故障排查

### 数据库未配置错误

**错误信息：** `数据库未配置`

**解决方案：** 
- 确认 `wrangler.toml` 中 D1 配置正确
- 确认 `database_id` 已填写
- 本地开发时，确保已运行初始化脚本

### 管理员密码错误

**错误信息：** `管理员密码错误`

**解决方案：**
- 本地：检查 `.dev.vars` 文件中的 `ADMIN_PASSWORD`
- 生产：重新设置密码 `wrangler secret put ADMIN_PASSWORD`

### 邀请码不存在

**错误信息：** `邀请码不存在`

**解决方案：**
- 在管理员后台生成新的邀请码
- 或通过数据库命令手动插入

## 性能优化

D1 数据库已创建以下索引以优化查询性能：

- `idx_invitation_codes_created` - 按创建时间排序邀请码
- `idx_invitation_codes_active` - 快速查找激活的邀请码
- `idx_fortune_records_invitation` - 根据邀请码查找记录
- `idx_fortune_records_created` - 按时间排序记录
- `idx_fortune_records_birth_date` - 按出生日期查询

## 安全建议

1. **管理员密码**
   - 使用强密码（至少 16 个字符）
   - 定期更换密码
   - 不要在代码中硬编码密码

2. **邀请码管理**
   - 定期审查未使用的邀请码
   - 及时禁用可疑邀请码
   - 为不同用途的邀请码添加备注

3. **数据访问**
   - 定期审查用户提交记录
   - 监控异常的高频提交
   - 注意保护用户隐私数据

## 技术支持

- Cloudflare D1 文档：https://developers.cloudflare.com/d1/
- Wrangler CLI 文档：https://developers.cloudflare.com/workers/wrangler/
