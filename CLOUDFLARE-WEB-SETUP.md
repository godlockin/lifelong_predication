# Cloudflare Web 界面配置指南

本指南将帮助您通过 Cloudflare Dashboard（Web 界面）完成所有配置，无需使用命令行。

## 📋 前提条件

- Cloudflare 账号
- 已登录 [Cloudflare Dashboard](https://dash.cloudflare.com/)

---

## 第一步：创建 D1 数据库

### 1.1 进入 D1 数据库页面

1. 登录 [Cloudflare Dashboard](https://dash.cloudflare.com/)
2. 在左侧菜单中找到 **Workers & Pages**
3. 点击顶部标签栏的 **D1 SQL Database**
4. 点击右上角的 **Create database** 按钮

### 1.2 创建数据库

1. **Database name**: 输入 `life-fortune-db`
2. **Location**: 选择 **Automatic**（或选择离您用户最近的区域）
3. 点击 **Create** 按钮

### 1.3 记录 Database ID

创建成功后，您会看到数据库详情页面。请记录以下信息：
- **Database name**: `life-fortune-db`
- **Database ID**: 类似 `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx` 的字符串

> ⚠️ 保存好 Database ID，后面需要用到！

---

## 第二步：初始化数据库表结构

### 2.1 进入数据库控制台

1. 在刚创建的数据库详情页面
2. 点击 **Console** 标签

### 2.2 执行 SQL 脚本

在控制台中，**复制并粘贴**以下完整的 SQL 脚本，然后点击 **Execute** 按钮：

```sql
-- 邀请码表
CREATE TABLE IF NOT EXISTS invitation_codes (
    code TEXT PRIMARY KEY,
    created_at TEXT NOT NULL,
    used_count INTEGER DEFAULT 0,
    last_used_at TEXT,
    is_active INTEGER DEFAULT 1,
    notes TEXT
);

CREATE INDEX IF NOT EXISTS idx_invitation_codes_created 
ON invitation_codes(created_at DESC);

CREATE INDEX IF NOT EXISTS idx_invitation_codes_active 
ON invitation_codes(is_active);

-- 命理计算记录表
CREATE TABLE IF NOT EXISTS fortune_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    invitation_code TEXT NOT NULL,
    birth_date TEXT NOT NULL,
    gender TEXT,
    city TEXT,
    longitude REAL,
    timezone INTEGER,
    bazi_result TEXT,
    ziwei_result TEXT,
    analysis_result TEXT,
    created_at TEXT NOT NULL,
    ip_address TEXT,
    user_agent TEXT,
    FOREIGN KEY (invitation_code) REFERENCES invitation_codes(code)
);

CREATE INDEX IF NOT EXISTS idx_fortune_records_invitation 
ON fortune_records(invitation_code);

CREATE INDEX IF NOT EXISTS idx_fortune_records_created 
ON fortune_records(created_at DESC);

CREATE INDEX IF NOT EXISTS idx_fortune_records_birth_date 
ON fortune_records(birth_date);
```

### 2.3 验证表创建成功

执行成功后，在控制台中运行以下查询来确认：

```sql
SELECT name FROM sqlite_master WHERE type='table';
```

您应该看到两个表：
- `invitation_codes`
- `fortune_records`

### 2.4 （可选）创建测试邀请码

在控制台中执行以下 SQL，创建 5 个测试邀请码：

```sql
INSERT INTO invitation_codes (code, created_at, notes) VALUES
('123456', datetime('now'), '测试邀请码 1'),
('234567', datetime('now'), '测试邀请码 2'),
('345678', datetime('now'), '测试邀请码 3'),
('456789', datetime('now'), '测试邀请码 4'),
('567890', datetime('now'), '测试邀请码 5');
```

验证插入成功：

```sql
SELECT code, created_at, notes FROM invitation_codes;
```

---

## 第三步：更新 wrangler.toml 配置

### 3.1 打开配置文件

在您的项目中，打开 `wrangler.toml` 文件。

### 3.2 填写 Database ID

找到文件底部的 D1 配置部分，将您在第一步记录的 `Database ID` 填入：

```toml
[[d1_databases]]
binding = "DB"
database_name = "life-fortune-db"
database_id = "在这里填写您的 Database ID"
```

**示例：**
```toml
[[d1_databases]]
binding = "DB"
database_name = "life-fortune-db"
database_id = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
```

保存文件。

---

## 第四步：配置环境变量（Secrets）

您有两个选择：

### 选择 A：本地开发（推荐先测试）

#### 4.1 创建 `.dev.vars` 文件

在项目根目录创建 `.dev.vars` 文件（如果不存在），添加以下内容：

```
GEMINI_API_KEY=your_gemini_api_key_here
ADMIN_PASSWORD=your_strong_password_here
```

**示例：**
```
GEMINI_API_KEY=AIzaSyC1234567890abcdefghijklmnopqrstuvwxyz
ADMIN_PASSWORD=MyStrongP@ssw0rd2024!
```

> ⚠️ 使用强密码，至少 16 个字符！

#### 4.2 本地测试

```bash
npm run dev
```

访问 http://localhost:8787/admin.html 测试管理员后台。

---

### 选择 B：生产环境部署

#### 4.1 通过 Web 界面设置 Secrets

1. 在 Cloudflare Dashboard 中，导航到 **Workers & Pages**
2. 如果您还没有部署 Worker，先跳到**第五步**部署，然后回来设置
3. 找到您的 Worker（例如 `life-fortune`）
4. 点击进入 Worker 详情页
5. 点击 **Settings** 标签
6. 在左侧菜单中选择 **Variables and Secrets**
7. 在 **Environment Variables** 部分，点击 **Add variable**

**添加第一个变量：**
- Variable name: `ADMIN_PASSWORD`
- Type: 选择 **Secret**（加密存储）
- Value: 输入您的管理员密码
- 点击 **Save**

**添加第二个变量：**
- Variable name: `GEMINI_API_KEY`
- Type: 选择 **Secret**
- Value: 输入您的 Gemini API Key
- 点击 **Save**

#### 4.2 应用变量

设置完成后，点击页面顶部的 **Deploy** 按钮使变量生效。

---

## 第五步：部署 Worker

### 方式一：使用命令行部署（推荐）

在项目目录中运行：

```bash
npm run deploy
```

### 方式二：通过 Web 界面部署

#### 5.1 创建 Worker

1. 在 Cloudflare Dashboard 中，导航到 **Workers & Pages**
2. 点击 **Create application**
3. 选择 **Create Worker**
4. Worker name: 输入 `life-fortune`（或您喜欢的名称）
5. 点击 **Deploy**

#### 5.2 上传代码（需要使用 wrangler deploy）

不幸的是，Cloudflare 目前不支持在 Web 界面直接上传完整的 Worker 项目。

**您仍需要运行一次命令来部署代码：**

```bash
npm run deploy
```

这是一次性操作。部署后，您可以在 Web 界面管理其他所有内容。

---

## 第六步：绑定 D1 数据库到 Worker

### 6.1 进入 Worker 设置

1. 在 **Workers & Pages** 页面
2. 点击您的 Worker（`life-fortune`）
3. 点击 **Settings** 标签

### 6.2 添加 D1 绑定

1. 在左侧菜单中选择 **Bindings**
2. 点击 **Add binding** 按钮
3. 选择绑定类型：**D1 database**
4. 填写信息：
   - **Variable name**: `DB`
   - **D1 database**: 从下拉菜单中选择 `life-fortune-db`
5. 点击 **Save**
6. 点击页面顶部的 **Deploy** 使绑定生效

> ✅ 如果您已经通过 `wrangler.toml` 配置并部署，这一步会自动完成，无需手动操作。

---

## 第七步：访问管理员后台

### 7.1 获取 Worker URL

部署成功后，在 Worker 详情页的顶部，您会看到类似的 URL：

```
https://life-fortune.your-subdomain.workers.dev
```

### 7.2 访问管理员后台

在浏览器中访问：

```
https://life-fortune.your-subdomain.workers.dev/admin.html
```

### 7.3 登录

使用您在第四步设置的 `ADMIN_PASSWORD` 登录。

---

## 第八步：使用管理员后台

### 8.1 生成邀请码

1. 登录成功后，您会看到"邀请码管理"标签
2. 输入生成数量（1-100）
3. 可选：添加备注
4. 点击"生成"按钮
5. 复制显示的邀请码

### 8.2 查看邀请码列表

- 在表格中查看所有邀请码
- 查看使用次数、创建时间、状态
- 使用分页浏览

### 8.3 查看用户记录

1. 切换到"用户记录"标签
2. 查看用户提交的命理计算记录
3. 点击"查看详情"按钮查看完整结果

---

## 第九步：在 Web 界面管理数据库

### 9.1 查看数据库数据

1. 回到 D1 数据库页面
2. 选择 `life-fortune-db`
3. 点击 **Console** 标签
4. 执行 SQL 查询

**常用查询：**

```sql
-- 查看所有邀请码
SELECT code, created_at, used_count, is_active, notes 
FROM invitation_codes 
ORDER BY created_at DESC;

-- 查看最近的用户提交
SELECT id, invitation_code, birth_date, gender, city, created_at 
FROM fortune_records 
ORDER BY created_at DESC 
LIMIT 20;

-- 统计邀请码使用情况
SELECT invitation_code, COUNT(*) as usage_count 
FROM fortune_records 
GROUP BY invitation_code 
ORDER BY usage_count DESC;
```

### 9.2 手动管理数据

**手动添加邀请码：**

```sql
INSERT INTO invitation_codes (code, created_at, notes) 
VALUES ('888888', datetime('now'), '特殊邀请码');
```

**禁用邀请码：**

```sql
UPDATE invitation_codes 
SET is_active = 0 
WHERE code = '888888';
```

**启用邀请码：**

```sql
UPDATE invitation_codes 
SET is_active = 1 
WHERE code = '888888';
```

**删除邀请码：**

```sql
DELETE FROM invitation_codes 
WHERE code = '888888';
```

---

## 第十步：监控和维护

### 10.1 查看 Worker 日志

1. 在 Worker 详情页
2. 点击 **Logs** 标签
3. 选择 **Begin log stream** 查看实时日志

### 10.2 查看 Worker 分析数据

1. 在 Worker 详情页
2. 点击 **Analytics** 标签
3. 查看请求量、错误率等指标

### 10.3 更新环境变量

如需更改管理员密码或 API Key：

1. 进入 Worker 的 **Settings** → **Variables and Secrets**
2. 找到要修改的变量
3. 点击 **Edit** 按钮
4. 输入新值
5. 点击 **Save**
6. 点击 **Deploy** 使更改生效

---

## 📊 Web 界面操作速查表

| 操作 | 位置 | 步骤 |
|------|------|------|
| 创建数据库 | Workers & Pages → D1 | Create database |
| 执行 SQL | D1 → 数据库名 → Console | 粘贴 SQL → Execute |
| 设置 Secrets | Worker → Settings → Variables | Add variable (Secret) |
| 绑定数据库 | Worker → Settings → Bindings | Add binding → D1 |
| 查看日志 | Worker → Logs | Begin log stream |
| 查看数据 | D1 → 数据库名 → Console | 执行 SELECT 查询 |

---

## 🆘 常见问题

### Q1: 我找不到 D1 Database 选项？

**答**: 确保您的 Cloudflare 账户已启用 Workers。如果是免费账户，D1 功能应该直接可用。

### Q2: 数据库创建成功，但 Worker 连接不上？

**答**: 
1. 检查 `wrangler.toml` 中的 `database_id` 是否正确
2. 检查 Worker Settings → Bindings 中是否正确绑定了 D1 数据库
3. 确保变量名是 `DB`（大写）

### Q3: 管理员后台无法登录？

**答**:
1. 检查 Worker Settings → Variables 中是否设置了 `ADMIN_PASSWORD`
2. 确保密码类型是 **Secret**
3. 设置后记得点击 Deploy 使其生效
4. 清除浏览器缓存重试

### Q4: 如何更改数据库区域？

**答**: 创建数据库时无法更改区域。如需更改，只能删除重建。建议选择 **Automatic** 让 Cloudflare 自动选择。

### Q5: 如何备份数据库？

**答**: 
1. 进入 D1 数据库控制台
2. 执行 `SELECT * FROM invitation_codes;`
3. 复制结果
4. 同样方式导出 `fortune_records` 表
5. 保存到本地文件

---

## ✅ 完成检查清单

- [ ] D1 数据库已创建（`life-fortune-db`）
- [ ] 数据库表结构已初始化（2个表，5个索引）
- [ ] 测试邀请码已创建（可选）
- [ ] `wrangler.toml` 已更新 `database_id`
- [ ] 环境变量已配置（`ADMIN_PASSWORD`, `GEMINI_API_KEY`）
- [ ] Worker 已部署
- [ ] D1 绑定已添加到 Worker
- [ ] 可以访问管理员后台
- [ ] 可以成功登录
- [ ] 可以生成邀请码
- [ ] 可以查看邀请码列表

---

## 🎉 大功告成！

现在您可以：
- ✅ 通过 Web 界面管理所有配置
- ✅ 使用管理员后台生成邀请码
- ✅ 在 D1 控制台直接查询和管理数据
- ✅ 通过 Dashboard 监控系统运行状态

**无需再使用命令行！**

如有问题，请参考：
- [完整文档](file:///Users/chenchen/working/sourcecode/tools/life/README-DB.md)
- [实现详情](file:///Users/chenchen/.gemini/antigravity/brain/60ce74c7-a654-4041-aa25-f703440d8e42/walkthrough.md)
