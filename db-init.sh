#!/bin/bash

# 命理测算系统 - 数据库初始化脚本
# 用于创建和初始化 Cloudflare D1 数据库

set -e  # 遇到错误立即退出

echo "🔮 命理测算系统 - 数据库初始化"
echo "================================"

# 1. 创建 D1 数据库
echo ""
echo "步骤 1: 创建 D1 数据库..."
echo "运行命令: wrangler d1 create life-fortune-db"
echo ""
echo "⚠️  请手动运行上述命令创建数据库，然后将返回的 database_id 更新到 wrangler.toml 文件中"
echo "   找到 wrangler.toml 中的 [[d1_databases]] 部分，填写 database_id"
echo ""
read -p "数据库是否已创建并且 wrangler.toml 已更新？(y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    echo "❌ 操作取消。请先创建数据库并更新配置。"
    exit 1
fi

# 2. 应用数据库架构
echo ""
echo "步骤 2: 应用数据库架构..."
wrangler d1 execute life-fortune-db --local --file=./schema.sql
echo "✅ 本地数据库架构已应用"

echo ""
read -p "是否也要应用到生产环境数据库？(y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
    wrangler d1 execute life-fortune-db --remote --file=./schema.sql
    echo "✅ 生产环境数据库架构已应用"
fi

# 3. 创建初始测试邀请码（仅本地）
echo ""
echo "步骤 3: 创建测试邀请码..."
read -p "是否创建 5 个测试邀请码到本地数据库？(y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
    wrangler d1 execute life-fortune-db --local --command="
    INSERT INTO invitation_codes (code, created_at, notes) VALUES
    ('123456', datetime('now'), '测试邀请码 1'),
    ('234567', datetime('now'), '测试邀请码 2'),
    ('345678', datetime('now'), '测试邀请码 3'),
    ('456789', datetime('now'), '测试邀请码 4'),
    ('567890', datetime('now'), '测试邀请码 5');
    "
    echo "✅ 测试邀请码已创建"
    echo ""
    echo "测试邀请码列表:"
    echo "  - 123456"
    echo "  - 234567"
    echo "  - 345678"
    echo "  - 456789"
    echo "  - 567890"
fi

echo ""
echo "================================"
echo "✅ 数据库初始化完成！"
echo ""
echo "下一步操作："
echo "1. 在 .dev.vars 文件中设置 ADMIN_PASSWORD（本地开发）"
echo "2. 运行 'npm run dev' 启动本地开发服务器"
echo "3. 访问 http://localhost:8787/admin.html 打开管理员后台"
echo "4. 生产环境部署前，请设置生产环境的管理员密码："
echo "   wrangler secret put ADMIN_PASSWORD"
echo ""
