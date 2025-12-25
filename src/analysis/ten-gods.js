/**
 * 十神分析模块
 * 
 * 十神是根据日干与其他干支的五行生克关系确定的
 */

import { STEM_ELEMENT, STEM_POLARITY, getStemElement, isStemYang } from '../core/heavenly-stems.js';
import { BRANCH_ELEMENT, getHiddenStems } from '../core/earthly-branches.js';

// 五行相生
const ELEMENT_GENERATE = {
    '木': '火', '火': '土', '土': '金', '金': '水', '水': '木'
};

// 五行相克
const ELEMENT_CONQUER = {
    '木': '土', '土': '水', '水': '火', '火': '金', '金': '木'
};

// 被生
const ELEMENT_GENERATED_BY = {
    '火': '木', '土': '火', '金': '土', '水': '金', '木': '水'
};

// 被克
const ELEMENT_CONQUERED_BY = {
    '土': '木', '水': '土', '火': '水', '金': '火', '木': '金'
};

/**
 * 十神名称
 * 根据五行关系和阴阳确定
 */
const TEN_GODS = {
    '同我同性': '比肩',   // 同五行同阴阳
    '同我异性': '劫财',   // 同五行异阴阳
    '我生同性': '食神',   // 我生同阴阳
    '我生异性': '伤官',   // 我生异阴阳
    '我克同性': '偏财',   // 我克同阴阳
    '我克异性': '正财',   // 我克异阴阳
    '克我同性': '七杀',   // 克我同阴阳（偏官）
    '克我异性': '正官',   // 克我异阴阳
    '生我同性': '偏印',   // 生我同阴阳（枭神）
    '生我异性': '正印'    // 生我异阴阳
};

// 十神简称
export const TEN_GOD_SHORT = {
    '比肩': '比', '劫财': '劫',
    '食神': '食', '伤官': '伤',
    '偏财': '偏财', '正财': '正财',
    '七杀': '杀', '正官': '官',
    '偏印': '枭', '正印': '印'
};

// 十神五行
export const TEN_GOD_ELEMENT = {
    '比肩': '同', '劫财': '同',
    '食神': '生', '伤官': '生',
    '偏财': '克', '正财': '克',
    '七杀': '被克', '正官': '被克',
    '偏印': '被生', '正印': '被生'
};

/**
 * 计算天干的十神
 * @param {string} dayStem - 日干（日主）
 * @param {string} targetStem - 目标天干
 * @returns {string} 十神名称
 */
export function calculateTenGod(dayStem, targetStem) {
    const dayElement = getStemElement(dayStem);
    const targetElement = getStemElement(targetStem);
    const dayYang = isStemYang(dayStem);
    const targetYang = isStemYang(targetStem);
    const samePolarity = dayYang === targetYang;

    let relation;

    if (dayElement === targetElement) {
        relation = samePolarity ? '同我同性' : '同我异性';
    } else if (ELEMENT_GENERATE[dayElement] === targetElement) {
        relation = samePolarity ? '我生同性' : '我生异性';
    } else if (ELEMENT_CONQUER[dayElement] === targetElement) {
        relation = samePolarity ? '我克同性' : '我克异性';
    } else if (ELEMENT_CONQUERED_BY[dayElement] === targetElement) {
        relation = samePolarity ? '克我同性' : '克我异性';
    } else if (ELEMENT_GENERATED_BY[dayElement] === targetElement) {
        relation = samePolarity ? '生我同性' : '生我异性';
    }

    return TEN_GODS[relation];
}

/**
 * 计算地支藏干的十神
 * @param {string} dayStem - 日干
 * @param {string} branch - 地支
 * @returns {Array<{stem: string, god: string}>} 藏干十神列表
 */
export function calculateBranchTenGods(dayStem, branch) {
    const hiddenStems = getHiddenStems(branch);
    return hiddenStems.map(stem => ({
        stem,
        god: calculateTenGod(dayStem, stem)
    }));
}

/**
 * 分析整个八字的十神
 * @param {Object} bazi - 八字对象
 * @returns {Object} 十神分析结果
 */
export function analyzeTenGods(bazi) {
    const dayStem = bazi.dayMaster;

    // 四柱天干十神
    const stemGods = {
        year: calculateTenGod(dayStem, bazi.yearPillar.stem),
        month: calculateTenGod(dayStem, bazi.monthPillar.stem),
        day: null, // 日干是日主本身
        hour: calculateTenGod(dayStem, bazi.hourPillar.stem)
    };

    // 四柱地支藏干十神
    const branchGods = {
        year: calculateBranchTenGods(dayStem, bazi.yearPillar.branch),
        month: calculateBranchTenGods(dayStem, bazi.monthPillar.branch),
        day: calculateBranchTenGods(dayStem, bazi.dayPillar.branch),
        hour: calculateBranchTenGods(dayStem, bazi.hourPillar.branch)
    };

    // 统计十神数量
    const godCount = {};

    // 统计天干十神
    [stemGods.year, stemGods.month, stemGods.hour].forEach(god => {
        if (god) {
            godCount[god] = (godCount[god] || 0) + 1;
        }
    });

    // 统计地支藏干十神（本气权重高）
    Object.values(branchGods).forEach(gods => {
        gods.forEach((g, i) => {
            const weight = i === 0 ? 1 : 0.5; // 本气权重1，中气余气0.5
            godCount[g.god] = (godCount[g.god] || 0) + weight;
        });
    });

    return {
        dayStem,
        stemGods,
        branchGods,
        godCount,

        // 便捷访问
        hasGod: (godName) => godCount[godName] > 0,
        getGodCount: (godName) => godCount[godName] || 0
    };
}

/**
 * 获取命局中最强的十神
 * @param {Object} godCount - 十神统计
 * @returns {string} 最强十神
 */
export function getStrongestGod(godCount) {
    let strongest = null;
    let maxCount = 0;

    for (const [god, count] of Object.entries(godCount)) {
        if (count > maxCount) {
            maxCount = count;
            strongest = god;
        }
    }

    return strongest;
}
