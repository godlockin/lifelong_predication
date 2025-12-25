/**
 * 刑冲合害分析模块
 */

import {
    BRANCH_SIX_COMBINE, BRANCH_SIX_COMBINE_RESULT,
    BRANCH_THREE_COMBINE_GROUPS, BRANCH_THREE_COMBINE,
    BRANCH_SIX_CLASH, BRANCH_THREE_PUNISHMENT, BRANCH_HARM,
    EARTHLY_BRANCHES
} from '../core/earthly-branches.js';
import { STEM_COMBINE, STEM_COMBINE_RESULT, STEM_CLASH } from '../core/heavenly-stems.js';

/**
 * 分析地支六合
 * @param {Array<string>} branches - 四柱地支
 * @returns {Array<Object>} 六合列表
 */
export function analyzeSixCombine(branches) {
    const combines = [];
    const positions = ['年支', '月支', '日支', '时支'];

    for (let i = 0; i < branches.length; i++) {
        for (let j = i + 1; j < branches.length; j++) {
            const b1 = branches[i];
            const b2 = branches[j];
            if (BRANCH_SIX_COMBINE[b1] === b2) {
                const key = [b1, b2].sort().join('');
                const result = BRANCH_SIX_COMBINE_RESULT[key] ||
                    BRANCH_SIX_COMBINE_RESULT[key.split('').reverse().join('')];
                combines.push({
                    type: '六合',
                    branches: [b1, b2],
                    positions: [positions[i], positions[j]],
                    result: result ? `合${result}` : '合',
                    description: `${positions[i]}${b1}与${positions[j]}${b2}六合`
                });
            }
        }
    }

    return combines;
}

/**
 * 分析地支三合
 * @param {Array<string>} branches - 四柱地支
 * @returns {Array<Object>} 三合列表
 */
export function analyzeThreeCombine(branches) {
    const combines = [];
    const branchSet = new Set(branches);

    for (const group of BRANCH_THREE_COMBINE_GROUPS) {
        const matching = group.filter(b => branchSet.has(b));
        if (matching.length >= 2) {
            const key = group.join('');
            const element = BRANCH_THREE_COMBINE[key];

            if (matching.length === 3) {
                combines.push({
                    type: '三合',
                    branches: matching,
                    result: `三合${element}局`,
                    description: `${matching.join('')}三合${element}局`
                });
            } else {
                combines.push({
                    type: '半合',
                    branches: matching,
                    result: `半合${element}局`,
                    description: `${matching.join('')}半合${element}局`
                });
            }
        }
    }

    return combines;
}

/**
 * 分析地支六冲
 * @param {Array<string>} branches - 四柱地支
 * @returns {Array<Object>} 六冲列表
 */
export function analyzeSixClash(branches) {
    const clashes = [];
    const positions = ['年支', '月支', '日支', '时支'];

    for (let i = 0; i < branches.length; i++) {
        for (let j = i + 1; j < branches.length; j++) {
            const b1 = branches[i];
            const b2 = branches[j];
            if (BRANCH_SIX_CLASH[b1] === b2) {
                clashes.push({
                    type: '六冲',
                    branches: [b1, b2],
                    positions: [positions[i], positions[j]],
                    description: `${positions[i]}${b1}与${positions[j]}${b2}相冲`,
                    interpretation: getClashInterpretation(positions[i], positions[j])
                });
            }
        }
    }

    return clashes;
}

/**
 * 分析地支三刑
 * @param {Array<string>} branches - 四柱地支
 * @returns {Array<Object>} 三刑列表
 */
export function analyzeThreePunishment(branches) {
    const punishments = [];
    const positions = ['年支', '月支', '日支', '时支'];

    // 寅巳申三刑
    const yinSiShen = ['寅', '巳', '申'];
    const yinSiShenMatching = yinSiShen.filter(b => branches.includes(b));
    if (yinSiShenMatching.length >= 2) {
        punishments.push({
            type: '无恩之刑',
            branches: yinSiShenMatching,
            description: `${yinSiShenMatching.join('')}相刑（无恩之刑）`
        });
    }

    // 丑戌未三刑
    const chouXuWei = ['丑', '戌', '未'];
    const chouXuWeiMatching = chouXuWei.filter(b => branches.includes(b));
    if (chouXuWeiMatching.length >= 2) {
        punishments.push({
            type: '恃势之刑',
            branches: chouXuWeiMatching,
            description: `${chouXuWeiMatching.join('')}相刑（恃势之刑）`
        });
    }

    // 子卯相刑
    if (branches.includes('子') && branches.includes('卯')) {
        punishments.push({
            type: '无礼之刑',
            branches: ['子', '卯'],
            description: '子卯相刑（无礼之刑）'
        });
    }

    // 自刑
    const selfPunishment = ['辰', '午', '酉', '亥'];
    selfPunishment.forEach(b => {
        const count = branches.filter(br => br === b).length;
        if (count >= 2) {
            punishments.push({
                type: '自刑',
                branches: [b, b],
                description: `${b}${b}自刑`
            });
        }
    });

    return punishments;
}

/**
 * 分析地支相害
 * @param {Array<string>} branches - 四柱地支
 * @returns {Array<Object>} 相害列表
 */
export function analyzeHarm(branches) {
    const harms = [];
    const positions = ['年支', '月支', '日支', '时支'];

    for (let i = 0; i < branches.length; i++) {
        for (let j = i + 1; j < branches.length; j++) {
            const b1 = branches[i];
            const b2 = branches[j];
            if (BRANCH_HARM[b1] === b2) {
                harms.push({
                    type: '相害',
                    branches: [b1, b2],
                    positions: [positions[i], positions[j]],
                    description: `${positions[i]}${b1}与${positions[j]}${b2}相害`
                });
            }
        }
    }

    return harms;
}

/**
 * 分析天干五合
 * @param {Array<string>} stems - 四柱天干
 * @returns {Array<Object>} 天干合列表
 */
export function analyzeStemCombine(stems) {
    const combines = [];
    const positions = ['年干', '月干', '日干', '时干'];

    for (let i = 0; i < stems.length; i++) {
        for (let j = i + 1; j < stems.length; j++) {
            const s1 = stems[i];
            const s2 = stems[j];
            if (STEM_COMBINE[s1] === s2) {
                const key = [s1, s2].sort().join('');
                const result = STEM_COMBINE_RESULT[key] ||
                    STEM_COMBINE_RESULT[key.split('').reverse().join('')];
                combines.push({
                    type: '天干合',
                    stems: [s1, s2],
                    positions: [positions[i], positions[j]],
                    result: result ? `合${result}` : '合',
                    description: `${positions[i]}${s1}与${positions[j]}${s2}相合`
                });
            }
        }
    }

    return combines;
}

/**
 * 综合刑冲合害分析
 * @param {Object} bazi - 八字对象
 * @returns {Object} 分析结果
 */
export function analyzeRelations(bazi) {
    const { stems, branches } = bazi;

    const sixCombines = analyzeSixCombine(branches);
    const threeCombines = analyzeThreeCombine(branches);
    const sixClashes = analyzeSixClash(branches);
    const punishments = analyzeThreePunishment(branches);
    const harms = analyzeHarm(branches);
    const stemCombines = analyzeStemCombine(stems);

    return {
        // 地支关系
        sixCombines,
        threeCombines,
        sixClashes,
        punishments,
        harms,
        // 天干关系
        stemCombines,
        // 汇总
        summary: {
            combines: [...sixCombines, ...threeCombines, ...stemCombines],
            conflicts: [...sixClashes, ...punishments, ...harms],
            hasCombine: sixCombines.length > 0 || threeCombines.length > 0,
            hasClash: sixClashes.length > 0,
            hasPunishment: punishments.length > 0,
            hasHarm: harms.length > 0
        }
    };
}

/**
 * 获取冲的解读
 */
function getClashInterpretation(pos1, pos2) {
    const interpretations = {
        '年支-月支': '年月冲，早年家境变动',
        '年支-日支': '年日冲，与祖辈或配偶关系需注意',
        '年支-时支': '年时冲，子女与长辈关系需调和',
        '月支-日支': '月日冲，事业与婚姻需平衡',
        '月支-时支': '月时冲，事业与子女需兼顾',
        '日支-时支': '日时冲，婚姻与子女关系需注意'
    };
    const key = `${pos1}-${pos2}`;
    return interpretations[key] || '';
}
