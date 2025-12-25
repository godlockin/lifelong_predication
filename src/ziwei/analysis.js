/**
 * 紫微斗数综合分析模块
 */

import { PALACE_MEANINGS } from './chart.js';

/**
 * 主星列表
 */
export const MAJOR_STARS = [
    '紫微', '天机', '太阳', '武曲', '天同', '廉贞', '天府',
    '太阴', '贪狼', '巨门', '天相', '天梁', '七杀', '破军'
];

/**
 * 辅星列表
 */
export const MINOR_STARS = [
    '左辅', '右弼', '文昌', '文曲', '天魁', '天钺', '禄存', '天马'
];

/**
 * 煞星列表
 */
export const SHA_STARS = [
    '擎羊', '陀罗', '火星', '铃星', '地空', '地劫'
];

/**
 * 星曜亮度等级
 */
export const STAR_BRIGHTNESS = ['庙', '旺', '得', '利', '平', '不', '陷'];

/**
 * 四化
 */
export const FOUR_TRANSFORMATIONS = ['化禄', '化权', '化科', '化忌'];

/**
 * 主星性质描述
 */
export const STAR_DESCRIPTIONS = {
    '紫微': { element: '土', nature: '帝星，尊贵，领导', traits: '高贵、有威严、好面子' },
    '天机': { element: '木', nature: '智星，聪慧，善变', traits: '聪明、多谋、灵活' },
    '太阳': { element: '火', nature: '光明，博爱，付出', traits: '热情、慷慨、主动' },
    '武曲': { element: '金', nature: '财星，刚毅，果断', traits: '务实、能干、重财' },
    '天同': { element: '水', nature: '福星，温和，享乐', traits: '温和、懒散、知足' },
    '廉贞': { element: '火', nature: '次桃花，复杂，多才', traits: '聪明、复杂、多才艺' },
    '天府': { element: '土', nature: '财库，稳重，保守', traits: '稳重、保守、守成' },
    '太阴': { element: '水', nature: '富星，柔美，内敛', traits: '温柔、细腻、内向' },
    '贪狼': { element: '木', nature: '桃花，才艺，欲望', traits: '多才、好色、贪婪' },
    '巨门': { element: '水', nature: '暗星，口才，是非', traits: '口才好、多疑、是非' },
    '天相': { element: '水', nature: '印星，辅佐，正直', traits: '正直、有礼、辅佐' },
    '天梁': { element: '土', nature: '荫星，老成，化解', traits: '稳重、老成、化解灾厄' },
    '七杀': { element: '金', nature: '将星，刚强，冲劲', traits: '刚烈、有冲劲、孤独' },
    '破军': { element: '水', nature: '耗星，变动，破旧', traits: '破旧立新、冲动、变动' }
};

/**
 * 分析命盘
 * @param {Object} chartSummary - 命盘摘要
 * @returns {Object} 分析结果
 */
export function analyzeZiweiChart(chartSummary) {
    if (!chartSummary || !chartSummary.palaces) {
        return { error: '命盘数据不完整' };
    }

    // 找到命宫
    const mingPalace = chartSummary.palaces.find(p => p.name === '命宫');
    const fuqiPalace = chartSummary.palaces.find(p => p.name === '夫妻宫');
    const caiboPalace = chartSummary.palaces.find(p => p.name === '财帛宫');
    const shiyePalace = chartSummary.palaces.find(p => p.name === '事业宫');

    return {
        // 命宫分析
        ming: mingPalace ? {
            stars: mingPalace.majorStars,
            minorStars: mingPalace.minorStars,
            interpretation: interpretPalace('命宫', mingPalace.majorStars)
        } : null,

        // 婚姻分析
        marriage: fuqiPalace ? {
            stars: fuqiPalace.majorStars,
            interpretation: interpretPalace('夫妻宫', fuqiPalace.majorStars)
        } : null,

        // 财运分析
        wealth: caiboPalace ? {
            stars: caiboPalace.majorStars,
            interpretation: interpretPalace('财帛宫', caiboPalace.majorStars)
        } : null,

        // 事业分析
        career: shiyePalace ? {
            stars: shiyePalace.majorStars,
            interpretation: interpretPalace('事业宫', shiyePalace.majorStars)
        } : null,

        // 五行局
        fiveElementsClass: chartSummary.fiveElementsClass,

        // 命主身主
        soul: chartSummary.soul,
        body: chartSummary.body
    };
}

/**
 * 解读宫位
 * @param {string} palaceName - 宫位名称
 * @param {Array<string>} stars - 主星列表
 * @returns {string} 解读
 */
function interpretPalace(palaceName, stars) {
    if (!stars || stars.length === 0) {
        return `${palaceName}无主星坐守，需借对宫星曜判断`;
    }

    const starDesc = stars.map(star => {
        const desc = STAR_DESCRIPTIONS[star];
        return desc ? `${star}(${desc.traits})` : star;
    }).join('、');

    return `${palaceName}有${starDesc}坐守`;
}

/**
 * 生成紫微斗数报告
 * @param {Object} chartData - 命盘数据
 * @returns {Object} 报告
 */
export function generateZiweiReport(chartData) {
    if (!chartData.success) {
        return {
            available: false,
            message: chartData.error || '紫微斗数排盘需要iztro库支持',
            recommendation: '请安装: npm install iztro'
        };
    }

    const analysis = analyzeZiweiChart(chartData.summary);

    return {
        available: true,
        basicInfo: {
            solarDate: chartData.summary.solarDate,
            lunarDate: chartData.summary.lunarDate,
            gender: chartData.summary.gender,
            fiveElementsClass: chartData.summary.fiveElementsClass,
            soul: chartData.summary.soul,
            body: chartData.summary.body
        },
        analysis,
        palaces: chartData.summary.palaces
    };
}
