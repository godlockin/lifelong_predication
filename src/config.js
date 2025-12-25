/**
 * 环境变量配置模块
 * 
 * 所有配置项都支持环境变量覆盖，并提供合理的默认值
 */

/**
 * 获取环境变量，支持 Cloudflare Workers 和 Node.js 环境
 * @param {string} key - 环境变量名
 * @param {string} defaultValue - 默认值
 * @param {Object} env - Cloudflare Workers 的 env 对象
 * @returns {string} 环境变量值
 */
export function getEnv(key, defaultValue = '', env = null) {
    // 优先使用 Cloudflare Workers 的 env
    if (env && env[key] !== undefined) {
        return env[key];
    }

    // Node.js 环境
    if (typeof process !== 'undefined' && process.env && process.env[key] !== undefined) {
        return process.env[key];
    }

    return defaultValue;
}

/**
 * 配置项定义
 */
export const CONFIG = {
    // ===== AI 配置 =====
    ai: {
        // API 密钥（无默认值，必须配置）
        apiKey: (env) => getEnv('GEMINI_API_KEY', '', env),

        // 模型选择
        model: (env) => getEnv('AI_MODEL', 'gemini-2.0-flash', env),

        // 请求超时（毫秒）
        timeout: (env) => parseInt(getEnv('AI_TIMEOUT', '30000', env), 10),

        // 生成温度
        temperature: (env) => parseFloat(getEnv('AI_TEMPERATURE', '0.7', env)),

        // 最大输出令牌数
        maxTokens: (env) => parseInt(getEnv('AI_MAX_TOKENS', '2048', env), 10)
    },

    // ===== 服务配置 =====
    server: {
        // 服务端口
        port: (env) => parseInt(getEnv('PORT', '8787', env), 10),

        // 跨域来源
        corsOrigin: (env) => getEnv('CORS_ORIGIN', '*', env)
    },

    // ===== 命理计算默认值 =====
    fortune: {
        // 默认时区
        defaultTimezone: (env) => parseInt(getEnv('DEFAULT_TIMEZONE', '8', env), 10),

        // 默认经度（东八区标准经度）
        defaultLongitude: (env) => parseFloat(getEnv('DEFAULT_LONGITUDE', '120', env))
    }
};

/**
 * 获取完整配置对象
 * @param {Object} env - Cloudflare Workers 的 env 对象
 * @returns {Object} 配置对象
 */
export function getConfig(env = null) {
    return {
        ai: {
            apiKey: CONFIG.ai.apiKey(env),
            model: CONFIG.ai.model(env),
            timeout: CONFIG.ai.timeout(env),
            temperature: CONFIG.ai.temperature(env),
            maxTokens: CONFIG.ai.maxTokens(env)
        },
        server: {
            port: CONFIG.server.port(env),
            corsOrigin: CONFIG.server.corsOrigin(env)
        },
        fortune: {
            defaultTimezone: CONFIG.fortune.defaultTimezone(env),
            defaultLongitude: CONFIG.fortune.defaultLongitude(env)
        }
    };
}

/**
 * 验证必需的配置项
 * @param {Object} config - 配置对象
 * @returns {Object} 验证结果
 */
export function validateConfig(config) {
    const errors = [];
    const warnings = [];

    // AI 密钥检查（警告，不是错误，因为可以使用模板报告）
    if (!config.ai.apiKey) {
        warnings.push('GEMINI_API_KEY 未设置，AI润色功能将使用模板报告');
    }

    return {
        valid: errors.length === 0,
        errors,
        warnings
    };
}
