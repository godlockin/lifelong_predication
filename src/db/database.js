/**
 * 数据库服务层
 * 提供邀请码管理和命理记录存储功能
 */

/**
 * 生成6位数字邀请码
 * @returns {string} 6位数字邀请码
 */
export function generateInvitationCode() {
    // 生成100000到999999之间的随机数
    const code = Math.floor(100000 + Math.random() * 900000).toString();
    return code;
}

/**
 * 创建邀请码
 * @param {D1Database} db - D1数据库实例
 * @param {string} code - 邀请码（可选，不提供则自动生成）
 * @param {string} notes - 备注（可选）
 * @returns {Promise<{success: boolean, code: string, message?: string}>}
 */
export async function createInvitationCode(db, code = null, notes = null) {
    try {
        const invitationCode = code || generateInvitationCode();
        const now = new Date().toISOString();

        // 检查邀请码是否已存在
        const existing = await db
            .prepare('SELECT code FROM invitation_codes WHERE code = ?')
            .bind(invitationCode)
            .first();

        if (existing) {
            return {
                success: false,
                code: invitationCode,
                message: '邀请码已存在'
            };
        }

        // 插入新邀请码
        await db
            .prepare('INSERT INTO invitation_codes (code, created_at, notes) VALUES (?, ?, ?)')
            .bind(invitationCode, now, notes)
            .run();

        return {
            success: true,
            code: invitationCode
        };
    } catch (error) {
        return {
            success: false,
            message: error.message
        };
    }
}

/**
 * 验证邀请码是否有效
 * @param {D1Database} db - D1数据库实例
 * @param {string} code - 邀请码
 * @param {string} backdoorCode - 后门邀请码（可选）
 * @returns {Promise<{valid: boolean, message?: string}>}
 */
export async function verifyInvitationCode(db, code, backdoorCode = null) {
    // 后门邀请码
    if (backdoorCode && code === backdoorCode) {
        return { valid: true, message: '测试通道' };
    }

    try {
        const result = await db
            .prepare('SELECT code, is_active, used_count FROM invitation_codes WHERE code = ?')
            .bind(code)
            .first();

        if (!result) {
            return { valid: false, message: '邀请码不存在' };
        }

        if (result.is_active !== 1) {
            return { valid: false, message: '邀请码已被禁用' };
        }

        if (result.used_count > 0) {
            return { valid: false, message: '邀请码已失效（已使用）' };
        }

        return { valid: true };
    } catch (error) {
        return { valid: false, message: error.message };
    }
}

/**
 * 使用邀请码（增加使用次数）
 * @param {D1Database} db - D1数据库实例
 * @param {string} code - 邀请码
 * @param {string} backdoorCode - 后门邀请码（可选）
 * @returns {Promise<{success: boolean, message?: string}>}
 */
export async function useInvitationCode(db, code, backdoorCode = null) {
    // 后门邀请码不消耗次数
    if (backdoorCode && code === backdoorCode) {
        return { success: true };
    }

    try {
        const now = new Date().toISOString();

        const result = await db
            .prepare(`
                UPDATE invitation_codes 
                SET used_count = used_count + 1, last_used_at = ?
                WHERE code = ? AND is_active = 1
            `)
            .bind(now, code)
            .run();

        if (result.meta.changes === 0) {
            return { success: false, message: '邀请码不存在或已被禁用' };
        }

        return { success: true };
    } catch (error) {
        return { success: false, message: error.message };
    }
}

/**
 * 保存命理计算记录
 * @param {D1Database} db - D1数据库实例
 * @param {Object} data - 记录数据
 * @returns {Promise<{success: boolean, id?: number, message?: string}>}
 */
export async function saveFortuneRecord(db, data) {
    try {
        const {
            invitationCode,
            birthDate,
            gender,
            city,
            longitude,
            timezone,
            baziResult,
            ziweiResult,
            analysisResult,
            ipAddress,
            userAgent
        } = data;

        const now = new Date().toISOString();

        const result = await db
            .prepare(`
                INSERT INTO fortune_records (
                    invitation_code, birth_date, gender, city, 
                    longitude, timezone, bazi_result, ziwei_result, 
                    analysis_result, created_at, ip_address, user_agent
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            `)
            .bind(
                invitationCode,
                birthDate,
                gender,
                city,
                longitude,
                timezone,
                JSON.stringify(baziResult),
                JSON.stringify(ziweiResult),
                JSON.stringify(analysisResult),
                now,
                ipAddress,
                userAgent
            )
            .run();

        return {
            success: true,
            id: result.meta.last_row_id
        };
    } catch (error) {
        return {
            success: false,
            message: error.message
        };
    }
}

/**
 * 获取邀请码列表
 * @param {D1Database} db - D1数据库实例
 * @param {number} limit - 每页数量
 * @param {number} offset - 偏移量
 * @returns {Promise<{success: boolean, data?: Array, total?: number, message?: string}>}
 */
export async function getInvitationCodes(db, limit = 50, offset = 0) {
    try {
        // 获取总数
        const countResult = await db
            .prepare('SELECT COUNT(*) as total FROM invitation_codes')
            .first();

        // 获取列表
        const { results } = await db
            .prepare(`
                SELECT code, created_at, used_count, last_used_at, is_active, notes
                FROM invitation_codes
                ORDER BY created_at DESC
                LIMIT ? OFFSET ?
            `)
            .bind(limit, offset)
            .all();

        return {
            success: true,
            data: results,
            total: countResult.total
        };
    } catch (error) {
        return {
            success: false,
            message: error.message
        };
    }
}

/**
 * 获取命理计算记录列表
 * @param {D1Database} db - D1数据库实例
 * @param {number} limit - 每页数量
 * @param {number} offset - 偏移量
 * @param {string} invitationCode - 筛选特定邀请码（可选）
 * @returns {Promise<{success: boolean, data?: Array, total?: number, message?: string}>}
 */
export async function getFortuneRecords(db, limit = 50, offset = 0, invitationCode = null) {
    try {
        let countQuery = 'SELECT COUNT(*) as total FROM fortune_records';
        let dataQuery = `
            SELECT id, invitation_code, birth_date, gender, city, 
                   longitude, timezone, created_at
            FROM fortune_records
        `;

        const bindings = [];

        if (invitationCode) {
            countQuery += ' WHERE invitation_code = ?';
            dataQuery += ' WHERE invitation_code = ?';
            bindings.push(invitationCode);
        }

        dataQuery += ' ORDER BY created_at DESC LIMIT ? OFFSET ?';

        // 获取总数
        const countResult = invitationCode
            ? await db.prepare(countQuery).bind(invitationCode).first()
            : await db.prepare(countQuery).first();

        // 获取列表
        const { results } = await db
            .prepare(dataQuery)
            .bind(...bindings, limit, offset)
            .all();

        return {
            success: true,
            data: results,
            total: countResult.total
        };
    } catch (error) {
        return {
            success: false,
            message: error.message
        };
    }
}

/**
 * 获取单个命理计算记录详情
 * @param {D1Database} db - D1数据库实例
 * @param {number} id - 记录ID
 * @returns {Promise<{success: boolean, data?: Object, message?: string}>}
 */
export async function getFortuneRecordDetail(db, id) {
    try {
        const result = await db
            .prepare(`
                SELECT id, invitation_code, birth_date, gender, city,
                       longitude, timezone, bazi_result, ziwei_result,
                       analysis_result, created_at, ip_address, user_agent
                FROM fortune_records
                WHERE id = ?
            `)
            .bind(id)
            .first();

        if (!result) {
            return { success: false, message: '记录不存在' };
        }

        // 解析JSON字段
        if (result.bazi_result) {
            result.bazi_result = JSON.parse(result.bazi_result);
        }
        if (result.ziwei_result) {
            result.ziwei_result = JSON.parse(result.ziwei_result);
        }
        if (result.analysis_result) {
            result.analysis_result = JSON.parse(result.analysis_result);
        }

        return {
            success: true,
            data: result
        };
    } catch (error) {
        return {
            success: false,
            message: error.message
        };
    }
}

/**
 * 禁用/启用邀请码
 * @param {D1Database} db - D1数据库实例
 * @param {string} code - 邀请码
 * @param {boolean} active - 是否激活
 * @returns {Promise<{success: boolean, message?: string}>}
 */
export async function setInvitationCodeStatus(db, code, active) {
    try {
        const result = await db
            .prepare('UPDATE invitation_codes SET is_active = ? WHERE code = ?')
            .bind(active ? 1 : 0, code)
            .run();

        if (result.meta.changes === 0) {
            return { success: false, message: '邀请码不存在' };
        }

        return { success: true };
    } catch (error) {
        return { success: false, message: error.message };
    }
}

/**
 * 删除邀请码
 * @param {D1Database} db - D1数据库实例
 * @param {string} code - 邀请码
 * @returns {Promise<{success: boolean, message?: string}>}
 */
export async function deleteInvitationCode(db, code) {
    try {
        // 先删除关联的记录
        await db.prepare('DELETE FROM fortune_records WHERE invitation_code = ?').bind(code).run();

        const result = await db
            .prepare('DELETE FROM invitation_codes WHERE code = ?')
            .bind(code)
            .run();

        if (result.meta.changes === 0) {
            return { success: false, message: '邀请码不存在' };
        }

        return { success: true };
    } catch (error) {
        return { success: false, message: error.message };
    }
}
