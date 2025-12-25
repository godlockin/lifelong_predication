# 快速开始指南

欢迎使用命理测算系统管理员功能！本指南将帮助您快速设置和使用数据库及管理员后台。

## 一、前提条件

确保已安装：
- Node.js >= 18.0.0
- npm
- Wrangler CLI (Cloudflare Workers CLI)

如果没有安装 Wrangler：
```bash
npm install -g wrangler
```

## 二、数据库初始化（5分钟）

### 步骤 1: 创建 D1 数据库

```bash
wrangler d1 create life-fortune-db
```

输出示例：
```
✅ Successfully created DB 'life-fortune-db'!

[[d1_databases]]
binding = "DB"
database_name = "life-fortune-db"
database_id = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
```

### 步骤 2: 更新配置

将返回的 `database_id` 填入 `wrangler.toml` 文件：

```toml
[[d1_databases]]
binding = "DB"
database_name = "life-fortune-db"
database_id = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"  # 👈 填写这里
```

### 步骤 3: 运行初始化脚本

```bash
./db-init.sh
```

按照提示完成初始化。建议：
- ✅ 应用架构到本地数据库
- ✅ 应用架构到生产数据库
- ✅ 创建5个测试邀请码（仅本地）

## 三、配置环境变量

### 本地开发

在 `.dev.vars` 文件中添加（如果文件不存在，创建它）：

```bash
GEMINI_API_KEY=your_gemini_api_key
ADMIN_PASSWORD=your_strong_password_here
```

> ⚠️ **重要**：密码至少使用16个字符，包含大小写字母、数字和特殊字符。

### 生产环境

部署前设置密码：

```bash
wrangler secret put ADMIN_PASSWORD
# 按提示输入密码

wrangler secret put GEMINI_API_KEY
# 按提示输入 API Key
```

## 四、启动本地开发服务器

```bash
npm run dev
```

服务器启动后，访问：
- **API**: http://localhost:8787/api
- **管理员后台**: http://localhost:8787/admin.html

## 五、使用管理员后台

### 1. 登录

访问 http://localhost:8787/admin.html

- 输入您在 `.dev.vars` 中设置的 `ADMIN_PASSWORD`
- 点击"登录"

### 2. 生成邀请码

在"邀请码管理"标签：
1. 输入生成数量（1-100）
2. 可选：添加备注
3. 点击"生成"
4. 复制显示的邀请码

### 3. 查看邀请码列表

- 查看所有邀请码
- 查看使用次数和状态
- 支持分页浏览

### 4. 查看用户记录

切换到"用户记录"标签：
- 查看用户提交的命理计算记录
- 点击"查看详情"查看完整的八字和紫微斗数结果

## 六、测试邀请码功能

### 验证邀请码

```bash
curl -X POST http://localhost:8787/verify-code \
  -H "Content-Type: application/json" \
  -d '{"code": "123456"}'
```

### 使用邀请码提交

```bash
curl -X POST http://localhost:8787/submit \
  -H "Content-Type: application/json" \
  -d '{
    "invitationCode": "123456",
    "birthDate": "2001-05-20T13:30:00",
    "gender": "男",
    "city": "北京"
  }'
```

## 七、生产部署

### 1. 确认数据库已初始化

```bash
# 查看数据库列表
wrangler d1 list

# 确认架构已应用
wrangler d1 execute life-fortune-db --remote --command="SELECT name FROM sqlite_master WHERE type='table';"
```

### 2. 设置生产环境密码

```bash
wrangler secret put ADMIN_PASSWORD
wrangler secret put GEMINI_API_KEY
```

### 3. 部署

```bash
npm run deploy
```

### 4. 访问生产环境

部署成功后，访问：
- `https://your-worker-name.your-subdomain.workers.dev/admin.html`

## 八、故障排查

### 数据库未配置

**错误**: `数据库未配置`

**解决**:
1. 确认 `wrangler.toml` 中 D1 配置正确
2. 确认 `database_id` 已填写
3. 本地开发时，确保运行了 `./db-init.sh`

### 管理员密码错误

**错误**: `管理员密码错误`

**解决**:
- 本地：检查 `.dev.vars` 文件中的 `ADMIN_PASSWORD`
- 生产：重新设置 `wrangler secret put ADMIN_PASSWORD`

### 邀请码不存在

**错误**: `邀请码不存在`

**解决**:
- 在管理员后台生成新的邀请码
- 或使用测试邀请码（如果创建了）

### 登录问题

**问题**: 无法登录管理员后台

**检查**:
1. `.dev.vars` 文件是否存在且包含 `ADMIN_PASSWORD`
2. 密码是否正确（注意大小写）
3. 浏览器控制台是否有错误信息

## 九、常用命令速查

```bash
# 本地开发
npm run dev

# 查看本地数据库中的邀请码
wrangler d1 execute life-fortune-db --local --command="SELECT * FROM invitation_codes;"

# 查看本地数据库中的用户记录
wrangler d1 execute life-fortune-db --local --command="SELECT id, invitation_code, birth_date, created_at FROM fortune_records;"

# 手动插入邀请码（本地）
wrangler d1 execute life-fortune-db --local --command="INSERT INTO invitation_codes (code, created_at) VALUES ('999999', datetime('now'));"

# 部署到生产环境
npm run deploy

# 查看生产环境数据库
wrangler d1 execute life-fortune-db --remote --command="SELECT COUNT(*) as total FROM invitation_codes;"
```

## 十、下一步

配置完成后，您可以：

1. **集成到前端应用**
   - 用户输入邀请码
   - 调用 `/verify-code` 验证
   - 调用 `/submit` 提交命理计算

2. **自定义界面**
   - 修改 `public/admin.html` 调整管理员后台样式
   - 添加更多统计功能

3. **增强功能**
   - 添加邀请码过期时间
   - 添加使用次数限制
   - 添加邮件通知

## 需要帮助？

查看完整文档：
- [数据库使用指南](file:///Users/chenchen/working/sourcecode/tools/life/README-DB.md)
- [实现详情](file:///Users/chenchen/.gemini/antigravity/brain/60ce74c7-a654-4041-aa25-f703440d8e42/walkthrough.md)

---

**祝使用愉快！🎉**
