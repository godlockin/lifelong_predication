/**
 * 综合命理解读模块
 * 
 * 整合八字分析、衍生分析和紫微斗数结果
 */

import { calculateBazi } from '../core/bazi.js';
import { analyzeTenGods } from '../analysis/ten-gods.js';
import { analyzeDayMasterStrength, getElementPreference, findMissingElements } from '../analysis/five-elements.js';
import { analyzeAllShensha } from '../derivatives/shensha.js';
import { analyzeNayin } from '../derivatives/nayin.js';
import { analyzeKongwang } from '../derivatives/kongwang.js';
import { analyzeRelations } from '../derivatives/relations.js';
import { generateZiweiChart } from '../ziwei/chart.js';
import { generateZiweiReport } from '../ziwei/analysis.js';
import { polishReport, createTemplateReport } from '../ai/polish.js';

/**
 * 进行完整的命理分析
 * @param {Object} params - 参数
 * @returns {Promise<Object>} 分析结果
 */
export async function performFullAnalysis(params) {
    const {
        birthDate,      // Date对象或ISO字符串
        longitude = 120, // 出生地经度，默认东八区标准经度
        timezone = 8,    // 时区，默认东八区
        gender = '男',   // 性别
        includeZiwei = true, // 是否包含紫微斗数
        apiKey = null,   // AI润色API密钥
        polish = false   // 是否进行AI润色
    } = params;

    // 解析日期
    const date = birthDate instanceof Date ? birthDate : new Date(birthDate);

    // ===== 八字分析 =====
    const bazi = calculateBazi(date, longitude, timezone);

    // 十神分析
    const tenGods = analyzeTenGods(bazi);

    // 五行旺衰
    const fiveElements = analyzeDayMasterStrength(bazi);
    const preference = getElementPreference(fiveElements);
    const missingElements = findMissingElements(bazi);

    // ===== 八字衍生分析 =====
    const shensha = analyzeAllShensha(bazi);
    const nayin = analyzeNayin(bazi);
    const kongwang = analyzeKongwang(bazi);
    const relations = analyzeRelations(bazi);

    // ===== 紫微斗数 =====
    let ziwei = null;
    if (includeZiwei) {
        const solarDate = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`;
        const chartData = await generateZiweiChart(solarDate, date.getHours(), gender);
        ziwei = generateZiweiReport(chartData);
    }

    // 组装分析结果
    const analysisResult = {
        // 基础信息
        input: {
            birthDate: date.toISOString(),
            longitude,
            timezone,
            gender
        },

        // 八字
        bazi: {
            pillars: bazi.bazi,
            yearPillar: bazi.yearPillar,
            monthPillar: bazi.monthPillar,
            dayPillar: bazi.dayPillar,
            hourPillar: bazi.hourPillar,
            dayMaster: bazi.dayMaster,
            trueSolarTime: bazi.trueSolarTime
        },

        // 十神
        tenGods: {
            stemGods: tenGods.stemGods,
            godCount: tenGods.godCount
        },

        // 五行
        fiveElements: {
            dayElement: fiveElements.dayElement,
            strength: fiveElements.strength,
            distribution: fiveElements.distribution,
            preference,
            missing: missingElements
        },

        // 衍生分析
        derivatives: {
            shensha,
            nayin,
            kongwang,
            relations
        },

        // 紫微斗数
        ziwei,

        // 生成时间
        generatedAt: new Date().toISOString()
    };

    // AI润色
    if (polish && apiKey) {
        const polished = await polishReport(analysisResult, {
            apiKey,
            type: 'comprehensive',
            tone: 'professional'
        });
        analysisResult.polishedReport = polished;
    } else {
        // 使用模板报告
        analysisResult.polishedReport = createTemplateReport(analysisResult);
    }

    return analysisResult;
}

/**
 * 快速八字分析（不含紫微和AI润色）
 * @param {Object} params - 参数
 * @returns {Object} 分析结果
 */
export function performQuickAnalysis(params) {
    const {
        birthDate,
        longitude = 120,
        timezone = 8
    } = params;

    const date = birthDate instanceof Date ? birthDate : new Date(birthDate);
    const bazi = calculateBazi(date, longitude, timezone);
    const tenGods = analyzeTenGods(bazi);
    const fiveElements = analyzeDayMasterStrength(bazi);
    const shensha = analyzeAllShensha(bazi);
    const nayin = analyzeNayin(bazi);

    return {
        bazi: bazi.bazi,
        dayMaster: bazi.dayMaster,
        strength: fiveElements.strength,
        tenGods: tenGods.godCount,
        shensha: shensha.summary.list,
        nayin: nayin.mainNayin
    };
}

/**
 * 仅排盘（返回基础八字数据）
 * @param {Object} params - 参数
 * @returns {Object} 八字数据
 */
export function calculateOnly(params) {
    const {
        birthDate,
        longitude = 120,
        timezone = 8
    } = params;

    const date = birthDate instanceof Date ? birthDate : new Date(birthDate);
    return calculateBazi(date, longitude, timezone);
}
