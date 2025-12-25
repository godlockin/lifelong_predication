/**
 * 管理员认证中间件
 */

/**
 * 验证管理员密码
 * @param {string} password - 提供的密码
 * @param {string} adminPassword - 正确的管理员密码
 * @returns {boolean}
 */
function verifyAdminPassword(password, adminPassword) {
    if (!adminPassword) {
        return false;
    }
    return password === adminPassword;
}

/**
 * 管理员认证中间件
 * 检查请求头中的 X-Admin-Password 是否匹配环境变量 ADMIN_PASSWORD
 */
export async function adminAuth(c, next) {
    const providedPassword = c.req.header('X-Admin-Password');
    const adminPassword = c.env.ADMIN_PASSWORD;

    if (!adminPassword) {
        return c.json({
            error: '服务器未配置管理员密码',
            message: '请在环境变量中设置 ADMIN_PASSWORD'
        }, 500);
    }

    if (!providedPassword) {
        return c.json({
            error: '未提供管理员密码',
            message: '请在请求头中添加 X-Admin-Password'
        }, 401);
    }

    if (!verifyAdminPassword(providedPassword, adminPassword)) {
        return c.json({
            error: '管理员密码错误',
            message: '认证失败'
        }, 401);
    }

    // 认证通过，继续处理请求
    await next();
}
