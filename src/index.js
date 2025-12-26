/**
 * 命理测算系统 API 入口  (修复后的版本)
 */

import { Hono } from 'hono';
import { cors } from 'hono/cors';
import { calculateBazi } from './core/bazi.js';
import { getSolarTimeDetails } from './core/solar-time.js';
import { getCityLocation, searchCities, getAllCities, CITY_HIERARCHY } from './data/cities.js';
import { performFullAnalysis, performQuickAnalysis } from './schools/comprehensive.js';
import { generateZiweiChart } from './ziwei/chart.js';
import { generateZiweiReport } from './ziwei/analysis.js';
import { polishReport, createTemplateReport } from './ai/polish.js';
import { getConfig } from './config.js';
import { adminAuth } from './middleware/auth.js';
import {
    createInvitationCode,
    verifyInvitationCode,
    useInvitationCode,
    saveFortuneRecord,
    getInvitationCodes,
    getFortuneRecords,
    getFortuneRecordDetail,
    setInvitationCodeStatus,
    deleteInvitationCode
} from './db/database.js';

const app = new Hono();

/**
 * 解析日期字符串为本地时间
 * 当输入格式为 "2001-05-20T13:30:00" 时，将其视为本地时间而非UTC
 * @param {string} dateString - 日期字符串
 * @returns {Date} 解析后的日期对象
 */
function parseLocalDateTime(dateString) {
    // 如果是没有时区信息的ISO格式字符串，手动解析为本地时间
    if (dateString.includes('T') && !dateString.includes('Z') &&
        !dateString.includes('+') && !dateString.includes('-', 10)) {
        const parts = dateString.match(/(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})/);
        if (parts) {
            return new Date(
                parseInt(parts[1]),      // 年
                parseInt(parts[2]) - 1,  // 月 (0-11)
                parseInt(parts[3]),      // 日
                parseInt(parts[4]),      // 时
                parseInt(parts[5]),      // 分
                parseInt(parts[6])       // 秒
            );
        }
    }
    return new Date(dateString);
}

// 启用CORS
app.use('/*', cors());

// API健康检查
app.get('/api', (c) => {
    const config = getConfig(c.env);
    return c.json({
        name: '命理测算系统',
        version: '1.0.0',
        description: '八字命理 + 紫微斗数 + AI润色',
        config: {
            aiModel: config.ai.model,
            hasApiKey: !!config.ai.apiKey,
            defaultTimezone: config.fortune.defaultTimezone,
            defaultLongitude: config.fortune.defaultLongitude
        },
        endpoints: {
            '/api': 'GET - API信息',
            '/calculate': 'POST - 八字排盘',
            '/analyze': 'POST - 完整命理分析',
            '/quick': 'POST - 快速分析',
            '/ziwei': 'POST - 紫微斗数排盘',
            '/cities': 'GET - 城市列表',
            '/cities/search': 'GET - 搜索城市',
            '/polish': 'POST - AI润色',
            '/verify-code': 'POST - 验证邀请码',
            '/submit': 'POST - 提交命理计算（需要邀请码）',
            '/admin/invitation-codes': 'POST/GET - 管理邀请码（需要管理员认证）',
            '/admin/records': 'GET - 查看用户记录（需要管理员认证）'
        }
    });
});

// 八字排盘
app.post('/calculate', async (c) => {
    try {
        const body = await c.req.json();
        const { birthDate, longitude, timezone, city } = body;

        if (!birthDate) {
            return c.json({ error: '请提供出生日期时间 (birthDate)' }, 400);
        }

        const config = getConfig(c.env);
        let lng = longitude;
        let tz = timezone || config.fortune.defaultTimezone;

        if (city && !longitude) {
            const cityData = getCityLocation(city);
            if (cityData) {
                lng = cityData.longitude;
                tz = cityData.timezone;
            }
        }

        lng = lng || config.fortune.defaultLongitude;
        const date = parseLocalDateTime(birthDate);


        const bazi = calculateBazi(date, lng, tz);
        const solarTimeDetails = getSolarTimeDetails(date, lng, tz);

        return c.json({
            success: true,
            data: {
                bazi: bazi.bazi,
                pillars: {
                    year: bazi.yearPillar,
                    month: bazi.monthPillar,
                    day: bazi.dayPillar,
                    hour: bazi.hourPillar
                },
                dayMaster: bazi.dayMaster,
                solarTime: solarTimeDetails
            }
        });
    } catch (error) {
        return c.json({ error: error.message }, 500);
    }
});

// 完整命理分析
app.post('/analyze', async (c) => {
    try {
        const body = await c.req.json();
        const {
            invitationCode,
            name,
            birthDate,
            longitude,
            timezone,
            city,
            gender = '男',
            includeZiwei = true,
            polish = false
        } = body;

        if (!invitationCode) {
            return c.json({ error: '请提供邀请码 (invitationCode)' }, 400);
        }

        if (!birthDate) {
            return c.json({ error: '请提供出生日期时间 (birthDate)' }, 400);
        }

        if (!c.env.DB) {
            return c.json({ error: '数据库未配置' }, 500);
        }

        // 验证邀请码
        const verification = await verifyInvitationCode(c.env.DB, invitationCode);
        if (!verification.valid) {
            return c.json({ error: verification.message }, 403);
        }

        const config = getConfig(c.env);
        let lng = longitude;
        let tz = timezone || config.fortune.defaultTimezone;

        if (city && !longitude) {
            const cityData = getCityLocation(city);
            if (cityData) {
                lng = cityData.longitude;
                tz = cityData.timezone;
            }
        }

        lng = lng || config.fortune.defaultLongitude;
        const apiKey = config.ai.apiKey || c.req.header('X-API-Key');

        const result = await performFullAnalysis({
            birthDate: parseLocalDateTime(birthDate),
            longitude: lng,
            timezone: tz,
            gender,
            includeZiwei,
            apiKey,
            polish: polish && !!apiKey
        });

        return c.json({
            success: true,
            data: result
        });
    } catch (error) {
        return c.json({ error: error.message }, 500);
    }
});

// 快速分析
app.post('/quick', async (c) => {
    try {
        const body = await c.req.json();
        const { birthDate, longitude, timezone, city } = body;

        if (!birthDate) {
            return c.json({ error: '请提供出生日期时间 (birthDate)' }, 400);
        }

        const config = getConfig(c.env);
        let lng = longitude;
        let tz = timezone || config.fortune.defaultTimezone;

        if (city && !longitude) {
            const cityData = getCityLocation(city);
            if (cityData) {
                lng = cityData.longitude;
                tz = cityData.timezone;
            }
        }

        const result = performQuickAnalysis({
            birthDate: parseLocalDateTime(birthDate),
            longitude: lng || config.fortune.defaultLongitude,
            timezone: tz
        });

        return c.json({
            success: true,
            data: result
        });
    } catch (error) {
        return c.json({ error: error.message }, 500);
    }
});

// 紫微斗数
app.post('/ziwei', async (c) => {
    try {
        const body = await c.req.json();
        const { birthDate, gender = '男' } = body;

        if (!birthDate) {
            return c.json({ error: '请提供出生日期时间 (birthDate)' }, 400);
        }

        const date = parseLocalDateTime(birthDate);
        const solarDate = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`;

        const chartData = await generateZiweiChart(solarDate, date.getHours(), gender);
        const report = generateZiweiReport(chartData);

        return c.json({
            success: true,
            data: report
        });
    } catch (error) {
        return c.json({ error: error.message }, 500);
    }
});

// 城市列表 (已废弃，前端直接加载 static/cities.json)
app.get('/cities', (c) => {
    // 兼容性保留，但返回空或提示
    return c.json({
        success: true,
        data: []
    });
});

// 搜索城市 (已废弃)
app.get('/cities/search', (c) => {
    return c.json({
        success: true,
        data: []
    });
});

// AI润色
app.post('/polish', async (c) => {
    try {
        const body = await c.req.json();
        const { analysisData, type = 'comprehensive', tone = 'professional' } = body;

        if (!analysisData) {
            return c.json({ error: '请提供分析数据 (analysisData)' }, 400);
        }

        const config = getConfig(c.env);
        const apiKey = config.ai.apiKey || c.req.header('X-API-Key');

        if (!apiKey) {
            const templateReport = createTemplateReport(analysisData);
            return c.json({
                success: true,
                data: templateReport
            });
        }

        const result = await polishReport(analysisData, {
            apiKey,
            type,
            tone,
            model: config.ai.model
        });

        return c.json({
            success: true,
            data: result
        });
    } catch (error) {
        return c.json({ error: error.message }, 500);
    }
});

// ==================== 邀请码相关端点 ====================

// 验证邀请码（公开端点）
app.post('/verify-code', async (c) => {
    try {
        const body = await c.req.json();
        const { code } = body;

        if (!code) {
            return c.json({ error: '请提供邀请码 (code)' }, 400);
        }

        if (!c.env.DB) {
            return c.json({ error: '数据库未配置' }, 500);
        }

        const result = await verifyInvitationCode(c.env.DB, code, c.env.BACKDOOR_CODE);

        return c.json({
            success: result.valid,
            message: result.message
        });
    } catch (error) {
        return c.json({ error: error.message }, 500);
    }
});

// 提交命理计算（需要邀请码）
app.post('/submit', async (c) => {
    try {
        const body = await c.req.json();
        const {
            invitationCode,
            name,
            birthDate,
            longitude,
            timezone,
            city,
            gender = '男',
            includeZiwei = true,
            polish = false
        } = body;

        if (!invitationCode) {
            return c.json({ error: '请提供邀请码 (invitationCode)' }, 400);
        }

        if (!birthDate) {
            return c.json({ error: '请提供出生日期时间 (birthDate)' }, 400);
        }

        if (!c.env.DB) {
            return c.json({ error: '数据库未配置' }, 500);
        }

        // 验证邀请码
        const verification = await verifyInvitationCode(c.env.DB, invitationCode, c.env.BACKDOOR_CODE);
        if (!verification.valid) {
            return c.json({ error: verification.message }, 403);
        }

        // 如果是后门邀请码，确保它存在于数据库中（满足外键约束）
        if (c.env.BACKDOOR_CODE && invitationCode === c.env.BACKDOOR_CODE) {
            await createInvitationCode(c.env.DB, invitationCode, 'System Backdoor');
        }

        // 执行命理分析
        const config = getConfig(c.env);
        let lng = longitude;
        let tz = timezone || config.fortune.defaultTimezone;

        if (city && !longitude) {
            const cityData = getCityLocation(city);
            if (cityData) {
                lng = cityData.longitude;
                tz = cityData.timezone;
            }
        }

        lng = lng || config.fortune.defaultLongitude;
        const apiKey = config.ai.apiKey || c.req.header('X-API-Key');

        const result = await performFullAnalysis({
            birthDate: parseLocalDateTime(birthDate),
            longitude: lng,
            timezone: tz,
            gender,
            includeZiwei,
            apiKey,
            polish: polish && !!apiKey
        });

        // 保存记录到数据库
        const saveResult = await saveFortuneRecord(c.env.DB, {
            invitationCode,
            name,
            birthDate,
            gender,
            city,
            longitude: lng,
            timezone: tz,
            baziResult: result.bazi,
            ziweiResult: result.ziwei,
            analysisResult: {
                tenGods: result.tenGods,
                fiveElements: result.fiveElements,
                derivatives: result.derivatives,
                polishedReport: result.polishedReport
            },
            ipAddress: c.req.header('CF-Connecting-IP'),
            userAgent: c.req.header('User-Agent')
        });

        if (!saveResult.success) {
            console.error('保存记录失败:', saveResult.message);
            return c.json({ error: '保存记录失败: ' + saveResult.message }, 500);
        }

        // 标记邀请码为已使用
        const useResult = await useInvitationCode(c.env.DB, invitationCode, c.env.BACKDOOR_CODE);
        if (!useResult.success) {
            console.error('更新邀请码状态失败:', useResult.message);
            // 这里不中断，因为记录已经保存成功
        }

        return c.json({
            success: true,
            data: result,
            recordId: saveResult.id
        });
    } catch (error) {
        return c.json({ error: error.message }, 500);
    }
});

// ==================== 管理员端点 ====================

// 创建邀请码（需要管理员认证）
app.post('/admin/invitation-codes', adminAuth, async (c) => {
    try {
        const body = await c.req.json().catch(() => ({}));
        const { count = 1, notes = null } = body;

        if (!c.env.DB) {
            return c.json({ error: '数据库未配置' }, 500);
        }

        if (count < 1 || count > 100) {
            return c.json({ error: '生成数量必须在 1-100 之间' }, 400);
        }

        const results = [];
        for (let i = 0; i < count; i++) {
            const result = await createInvitationCode(c.env.DB, null, notes);
            results.push(result);
        }

        const successful = results.filter(r => r.success);
        const failed = results.filter(r => !r.success);

        return c.json({
            success: true,
            data: {
                created: successful.length,
                failed: failed.length,
                codes: successful.map(r => r.code),
                errors: failed.map(r => ({ code: r.code, message: r.message }))
            }
        });
    } catch (error) {
        return c.json({ error: error.message }, 500);
    }
});

// 获取邀请码列表（需要管理员认证）
app.get('/admin/invitation-codes', adminAuth, async (c) => {
    try {
        if (!c.env.DB) {
            return c.json({ error: '数据库未配置' }, 500);
        }

        const limit = parseInt(c.req.query('limit') || '50');
        const offset = parseInt(c.req.query('offset') || '0');

        const result = await getInvitationCodes(c.env.DB, limit, offset);

        if (!result.success) {
            return c.json({ error: result.message }, 500);
        }

        return c.json({
            success: true,
            data: result.data,
            total: result.total,
            limit,
            offset
        });
    } catch (error) {
        return c.json({ error: error.message }, 500);
    }
});

// 禁用/启用邀请码（需要管理员认证）
app.patch('/admin/invitation-codes/:code', adminAuth, async (c) => {
    try {
        const code = c.req.param('code');
        const body = await c.req.json();
        const { active } = body;

        if (!c.env.DB) {
            return c.json({ error: '数据库未配置' }, 500);
        }

        if (typeof active !== 'boolean') {
            return c.json({ error: '请提供 active 参数（true/false）' }, 400);
        }

        const result = await setInvitationCodeStatus(c.env.DB, code, active);

        if (!result.success) {
            return c.json({ error: result.message }, 404);
        }

        return c.json({
            success: true,
            message: active ? '邀请码已启用' : '邀请码已禁用'
        });
    } catch (error) {
        return c.json({ error: error.message }, 500);
    }
});

// 删除邀请码（需要管理员认证）
app.delete('/admin/invitation-codes/:code', adminAuth, async (c) => {
    try {
        const code = c.req.param('code');

        if (!c.env.DB) {
            return c.json({ error: '数据库未配置' }, 500);
        }

        const result = await deleteInvitationCode(c.env.DB, code);

        if (!result.success) {
            return c.json({ error: result.message }, 404);
        }

        return c.json({
            success: true,
            message: '邀请码已删除'
        });
    } catch (error) {
        return c.json({ error: error.message }, 500);
    }
});

// 获取用户记录列表（需要管理员认证）
app.get('/admin/records', adminAuth, async (c) => {
    try {
        if (!c.env.DB) {
            return c.json({ error: '数据库未配置' }, 500);
        }

        const limit = parseInt(c.req.query('limit') || '50');
        const offset = parseInt(c.req.query('offset') || '0');
        const invitationCode = c.req.query('code') || null;

        const result = await getFortuneRecords(c.env.DB, limit, offset, invitationCode);

        if (!result.success) {
            return c.json({ error: result.message }, 500);
        }

        return c.json({
            success: true,
            data: result.data,
            total: result.total,
            limit,
            offset
        });
    } catch (error) {
        return c.json({ error: error.message }, 500);
    }
});

// 获取单个记录详情（需要管理员认证）
app.get('/admin/records/:id', adminAuth, async (c) => {
    try {
        const id = parseInt(c.req.param('id'));

        if (!c.env.DB) {
            return c.json({ error: '数据库未配置' }, 500);
        }

        const result = await getFortuneRecordDetail(c.env.DB, id);

        if (!result.success) {
            return c.json({ error: result.message }, 404);
        }

        return c.json({
            success: true,
            data: result.data
        });
    } catch (error) {
        return c.json({ error: error.message }, 500);
    }
});

// ==================== 静态文件处理（放在所有路由最后作为fallback） ====================

// 处理所有未匹配的路由 - 尝试返回静态文件
app.get('*', async (c) => {
    const url = new URL(c.req.url);
    const pathname = url.pathname;

    // 如果是根路径，返回 index.html
    if (pathname === '/') {
        try {
            const indexUrl = new URL('/index.html', url.origin);
            const asset = await c.env.ASSETS.fetch(indexUrl.toString());
            if (asset.ok) {
                return new Response(asset.body, {
                    headers: asset.headers
                });
            }
        } catch (e) {
            console.error('Failed to fetch index.html:', e);
        }
    }

    // 尝试返回请求的静态文件
    try {
        const asset = await c.env.ASSETS.fetch(c.req.url);
        if (asset.ok) {
            return new Response(asset.body, {
                headers: asset.headers
            });
        }
    } catch (e) {
        console.error('Failed to fetch asset:', e);
    }

    // 如果静态文件不存在，返回 404
    return c.json({ error: 'Not found' }, 404);
});

export default app;
