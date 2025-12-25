/**
 * 空亡分析模块
 */

import { EARTHLY_BRANCHES, BRANCH_INDEX } from '../core/earthly-branches.js';
import { HEAVENLY_STEMS, STEM_INDEX } from '../core/heavenly-stems.js';

/**
 * 十个旬的空亡地支
 * 六十甲子分为六旬，每旬十天干配十地支，余两个地支为空亡
 */
const XUN_KONGWANG = {
    '甲子': ['戌', '亥'], '甲戌': ['申', '酉'], '甲申': ['午', '未'],
    '甲午': ['辰', '巳'], '甲辰': ['寅', '卯'], '甲寅': ['子', '丑']
};

// 计算干支所在的旬首
const XUN_MAP = {
    0: '甲子', 10: '甲戌', 20: '甲申', 30: '甲午', 40: '甲辰', 50: '甲寅'
};

/**
 * 计算干支的六十甲子序号
 * @param {string} stem - 天干
 * @param {string} branch - 地支
 * @returns {number} 序号 (0-59)
 */
function getJiaziIndex(stem, branch) {
    const stemIdx = STEM_INDEX[stem];
    const branchIdx = BRANCH_INDEX[branch];

    // 天干索引和地支索引的最小公倍数是60
    // 找到满足条件的序号
    for (let i = 0; i < 60; i++) {
        if (i % 10 === stemIdx && i % 12 === branchIdx) {
            return i;
        }
    }
    return 0;
}

/**
 * 获取干支所在的旬首
 * @param {string} ganzhi - 干支
 * @returns {string} 旬首
 */
export function getXunShou(ganzhi) {
    const stem = ganzhi[0];
    const branch = ganzhi[1];
    const idx = getJiaziIndex(stem, branch);
    const xunIdx = Math.floor(idx / 10) * 10;
    return XUN_MAP[xunIdx];
}

/**
 * 获取干支的旬空
 * @param {string} ganzhi - 干支
 * @returns {Array<string>} 空亡地支
 */
export function getKongwang(ganzhi) {
    const xunShou = getXunShou(ganzhi);
    return XUN_KONGWANG[xunShou] || [];
}

/**
 * 分析八字空亡
 * @param {Object} bazi - 八字对象
 * @returns {Object} 空亡分析结果
 */
export function analyzeKongwang(bazi) {
    // 以日柱查旬空
    const dayGanzhi = bazi.dayPillar.ganzhi;
    const kongwang = getKongwang(dayGanzhi);
    const xunShou = getXunShou(dayGanzhi);

    // 检查四柱地支是否落空亡
    const pillarNames = ['年支', '月支', '日支', '时支'];
    const kongwangPillars = [];

    bazi.branches.forEach((branch, i) => {
        if (kongwang.includes(branch)) {
            kongwangPillars.push({
                position: pillarNames[i],
                branch,
                interpretation: getKongwangInterpretation(pillarNames[i])
            });
        }
    });

    return {
        xunShou,
        kongwang,
        kongwangPillars,
        hasKongwang: kongwangPillars.length > 0,
        summary: kongwangPillars.length > 0
            ? `日柱${dayGanzhi}属${xunShou}旬，空亡${kongwang.join('、')}。${kongwangPillars.map(p => p.position).join('、')}落空亡。`
            : `日柱${dayGanzhi}属${xunShou}旬，空亡${kongwang.join('、')}，四柱无空亡。`
    };
}

/**
 * 获取空亡解读
 * @param {string} position - 位置
 * @returns {string} 解读
 */
function getKongwangInterpretation(position) {
    const interpretations = {
        '年支': '与祖上缘薄，少年运势起伏',
        '月支': '与父母兄弟缘薄，事业需靠自己',
        '日支': '婚姻感情需注意，配偶缘分特殊',
        '时支': '与子女缘分需努力经营，晚年注意'
    };
    return interpretations[position] || '';
}
