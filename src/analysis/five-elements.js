/**
 * 五行分析模块
 * 
 * 分析命局五行力量分布和日主旺衰
 */

import { STEM_ELEMENT } from '../core/heavenly-stems.js';
import { BRANCH_ELEMENT, getHiddenStems } from '../core/earthly-branches.js';

// 五行列表
export const FIVE_ELEMENTS = ['木', '火', '土', '金', '水'];

// 五行相生
export const ELEMENT_GENERATE = {
    '木': '火', '火': '土', '土': '金', '金': '水', '水': '木'
};

// 五行相克
export const ELEMENT_CONQUER = {
    '木': '土', '土': '水', '水': '火', '火': '金', '金': '木'
};

// 月支当令五行力量加成
const MONTH_POWER_BONUS = 3;

// 天干力量基准值
const STEM_BASE_POWER = 1;

// 地支藏干力量 [本气, 中气, 余气]
const HIDDEN_STEM_POWER = [1, 0.5, 0.3];

/**
 * 计算五行力量分布
 * @param {Object} bazi - 八字对象
 * @returns {Object} 五行力量
 */
export function calculateElementPower(bazi) {
    const power = { '木': 0, '火': 0, '土': 0, '金': 0, '水': 0 };

    // 天干五行力量
    bazi.stems.forEach(stem => {
        const element = STEM_ELEMENT[stem];
        power[element] += STEM_BASE_POWER;
    });

    // 地支藏干五行力量
    bazi.branches.forEach((branch, index) => {
        const hiddenStems = getHiddenStems(branch);
        const isMonthBranch = index === 1; // 月支

        hiddenStems.forEach((stem, i) => {
            const element = STEM_ELEMENT[stem];
            let p = HIDDEN_STEM_POWER[i] || 0.3;

            // 月支当令加成
            if (isMonthBranch && i === 0) {
                p += MONTH_POWER_BONUS;
            }

            power[element] += p;
        });
    });

    return power;
}

/**
 * 判断日主旺衰
 * @param {Object} bazi - 八字对象
 * @returns {Object} 旺衰分析结果
 */
export function analyzeDayMasterStrength(bazi) {
    const dayElement = STEM_ELEMENT[bazi.dayMaster];
    const power = calculateElementPower(bazi);

    // 计算帮助日主的力量（同五行 + 生我的五行）
    let helpPower = power[dayElement];

    // 生我的五行
    for (const [element, generates] of Object.entries(ELEMENT_GENERATE)) {
        if (generates === dayElement) {
            helpPower += power[element] * 0.7; // 生我的力量打折
        }
    }

    // 计算克泄日主的力量
    let drainPower = 0;

    // 我生的五行（泄我）
    const iGenerate = ELEMENT_GENERATE[dayElement];
    drainPower += power[iGenerate] * 0.8;

    // 我克的五行（耗我）
    const iConquer = ELEMENT_CONQUER[dayElement];
    drainPower += power[iConquer] * 0.5;

    // 克我的五行
    for (const [element, conquers] of Object.entries(ELEMENT_CONQUER)) {
        if (conquers === dayElement) {
            drainPower += power[element];
        }
    }

    // 判断旺衰
    const ratio = helpPower / (helpPower + drainPower);
    let strength;

    if (ratio >= 0.6) {
        strength = '旺';
    } else if (ratio >= 0.45) {
        strength = '中和';
    } else {
        strength = '弱';
    }

    return {
        dayElement,
        power,
        helpPower: Math.round(helpPower * 10) / 10,
        drainPower: Math.round(drainPower * 10) / 10,
        ratio: Math.round(ratio * 100) / 100,
        strength,
        isStrong: ratio >= 0.5,

        // 五行分布百分比
        distribution: Object.fromEntries(
            Object.entries(power).map(([e, p]) => [
                e,
                Math.round(p / Object.values(power).reduce((a, b) => a + b, 0) * 100)
            ])
        )
    };
}

/**
 * 分析五行缺失
 * @param {Object} bazi - 八字对象
 * @returns {Array<string>} 缺失的五行
 */
export function findMissingElements(bazi) {
    const power = calculateElementPower(bazi);
    return FIVE_ELEMENTS.filter(e => power[e] < 0.5);
}

/**
 * 获取五行喜忌
 * @param {Object} strengthAnalysis - 旺衰分析结果
 * @returns {Object} 喜忌五行
 */
export function getElementPreference(strengthAnalysis) {
    const { dayElement, isStrong } = strengthAnalysis;

    // 生我的五行
    let generatesMe;
    for (const [element, generates] of Object.entries(ELEMENT_GENERATE)) {
        if (generates === dayElement) {
            generatesMe = element;
            break;
        }
    }

    // 我生的五行
    const iGenerate = ELEMENT_GENERATE[dayElement];

    // 克我的五行
    let conquersMe;
    for (const [element, conquers] of Object.entries(ELEMENT_CONQUER)) {
        if (conquers === dayElement) {
            conquersMe = element;
            break;
        }
    }

    // 我克的五行
    const iConquer = ELEMENT_CONQUER[dayElement];

    if (isStrong) {
        // 身旺喜克泄耗
        return {
            favorable: [conquersMe, iGenerate, iConquer],
            unfavorable: [dayElement, generatesMe],
            description: '身旺宜克泄耗'
        };
    } else {
        // 身弱喜生扶
        return {
            favorable: [dayElement, generatesMe],
            unfavorable: [conquersMe, iGenerate, iConquer],
            description: '身弱宜生扶'
        };
    }
}
