/**
 * 神煞分析模块
 * 
 * 命局中的特殊符号系统
 */

import { HEAVENLY_STEMS, STEM_INDEX } from '../core/heavenly-stems.js';
import { EARTHLY_BRANCHES, BRANCH_INDEX } from '../core/earthly-branches.js';

/**
 * 天乙贵人查法
 * 甲戊庚牛羊，乙己鼠猴乡，丙丁猪鸡位，壬癸兔蛇藏，六辛逢马虎，此是贵人方
 */
const TIANYI_GUIREN = {
    '甲': ['丑', '未'], '戊': ['丑', '未'], '庚': ['丑', '未'],
    '乙': ['子', '申'], '己': ['子', '申'],
    '丙': ['亥', '酉'], '丁': ['亥', '酉'],
    '壬': ['卯', '巳'], '癸': ['卯', '巳'],
    '辛': ['午', '寅']
};

/**
 * 文昌贵人
 * 甲乙巳午报君知，丙戊申宫丁己鸡，庚亥辛子壬逢寅，癸卯只从卯上骑
 */
const WENCHANG = {
    '甲': '巳', '乙': '午', '丙': '申', '丁': '酉',
    '戊': '申', '己': '酉', '庚': '亥', '辛': '子',
    '壬': '寅', '癸': '卯'
};

/**
 * 驿马
 * 申子辰马在寅，寅午戌马在申，巳酉丑马在亥，亥卯未马在巳
 */
const YIMA_GROUPS = {
    '申子辰': '寅',
    '寅午戌': '申',
    '巳酉丑': '亥',
    '亥卯未': '巳'
};

/**
 * 桃花（咸池）
 * 申子辰在酉，寅午戌在卯，巳酉丑在午，亥卯未在子
 */
const TAOHUA_GROUPS = {
    '申子辰': '酉',
    '寅午戌': '卯',
    '巳酉丑': '午',
    '亥卯未': '子'
};

/**
 * 华盖
 * 申子辰华盖在辰，寅午戌华盖在戌，巳酉丑华盖在丑，亥卯未华盖在未
 */
const HUAGAI_GROUPS = {
    '申子辰': '辰',
    '寅午戌': '戌',
    '巳酉丑': '丑',
    '亥卯未': '未'
};

/**
 * 将星
 * 申子辰将星在子，寅午戌将星在午，巳酉丑将星在酉，亥卯未将星在卯
 */
const JIANGXING_GROUPS = {
    '申子辰': '子',
    '寅午戌': '午',
    '巳酉丑': '酉',
    '亥卯未': '卯'
};

/**
 * 羊刃
 * 根据日干确定，日干临帝旺之地
 */
const YANGREN = {
    '甲': '卯', '乙': '寅',
    '丙': '午', '丁': '巳',
    '戊': '午', '己': '巳',
    '庚': '酉', '辛': '申',
    '壬': '子', '癸': '亥'
};

/**
 * 根据年支/日支查找三合局对应的神煞
 */
function findByThreeHarmony(branch, groupMap) {
    for (const [group, result] of Object.entries(groupMap)) {
        if (group.includes(branch)) {
            return result;
        }
    }
    return null;
}

/**
 * 分析天乙贵人
 */
export function analyzeTianyiGuiren(bazi) {
    const guirenBranches = TIANYI_GUIREN[bazi.dayMaster] || [];
    const found = [];

    bazi.branches.forEach((branch, i) => {
        if (guirenBranches.includes(branch)) {
            found.push({
                position: ['年支', '月支', '日支', '时支'][i],
                branch
            });
        }
    });

    return {
        name: '天乙贵人',
        description: '逢凶化吉，贵人相助',
        guirenBranches,
        found,
        hasThis: found.length > 0
    };
}

/**
 * 分析文昌贵人
 */
export function analyzeWenchang(bazi) {
    const wenchangBranch = WENCHANG[bazi.dayMaster];
    const found = [];

    bazi.branches.forEach((branch, i) => {
        if (branch === wenchangBranch) {
            found.push({
                position: ['年支', '月支', '日支', '时支'][i],
                branch
            });
        }
    });

    return {
        name: '文昌贵人',
        description: '聪明好学，文才出众',
        wenchangBranch,
        found,
        hasThis: found.length > 0
    };
}

/**
 * 分析驿马
 */
export function analyzeYima(bazi) {
    const yearBranch = bazi.yearPillar.branch;
    const dayBranch = bazi.dayPillar.branch;

    const yimaByYear = findByThreeHarmony(yearBranch, YIMA_GROUPS);
    const yimaByDay = findByThreeHarmony(dayBranch, YIMA_GROUPS);

    const found = [];
    bazi.branches.forEach((branch, i) => {
        if (branch === yimaByYear || branch === yimaByDay) {
            found.push({
                position: ['年支', '月支', '日支', '时支'][i],
                branch
            });
        }
    });

    return {
        name: '驿马',
        description: '主迁移变动，奔波在外',
        yimaBranches: [yimaByYear, yimaByDay].filter(Boolean),
        found,
        hasThis: found.length > 0
    };
}

/**
 * 分析桃花
 */
export function analyzeTaohua(bazi) {
    const yearBranch = bazi.yearPillar.branch;
    const dayBranch = bazi.dayPillar.branch;

    const taohuaByYear = findByThreeHarmony(yearBranch, TAOHUA_GROUPS);
    const taohuaByDay = findByThreeHarmony(dayBranch, TAOHUA_GROUPS);

    const found = [];
    bazi.branches.forEach((branch, i) => {
        if (branch === taohuaByYear || branch === taohuaByDay) {
            found.push({
                position: ['年支', '月支', '日支', '时支'][i],
                branch
            });
        }
    });

    return {
        name: '桃花',
        description: '异性缘佳，魅力出众',
        taohuaBranches: [taohuaByYear, taohuaByDay].filter(Boolean),
        found,
        hasThis: found.length > 0
    };
}

/**
 * 分析华盖
 */
export function analyzeHuagai(bazi) {
    const yearBranch = bazi.yearPillar.branch;
    const dayBranch = bazi.dayPillar.branch;

    const huagaiByYear = findByThreeHarmony(yearBranch, HUAGAI_GROUPS);
    const huagaiByDay = findByThreeHarmony(dayBranch, HUAGAI_GROUPS);

    const found = [];
    bazi.branches.forEach((branch, i) => {
        if (branch === huagaiByYear || branch === huagaiByDay) {
            found.push({
                position: ['年支', '月支', '日支', '时支'][i],
                branch
            });
        }
    });

    return {
        name: '华盖',
        description: '聪慧孤高，适合艺术宗教',
        huagaiBranches: [huagaiByYear, huagaiByDay].filter(Boolean),
        found,
        hasThis: found.length > 0
    };
}

/**
 * 分析羊刃
 */
export function analyzeYangren(bazi) {
    const yangrenBranch = YANGREN[bazi.dayMaster];
    const found = [];

    bazi.branches.forEach((branch, i) => {
        if (branch === yangrenBranch) {
            found.push({
                position: ['年支', '月支', '日支', '时支'][i],
                branch
            });
        }
    });

    return {
        name: '羊刃',
        description: '刚烈果断，宜制化',
        yangrenBranch,
        found,
        hasThis: found.length > 0
    };
}

/**
 * 分析将星
 */
export function analyzeJiangxing(bazi) {
    const yearBranch = bazi.yearPillar.branch;
    const dayBranch = bazi.dayPillar.branch;

    const jiangxingByYear = findByThreeHarmony(yearBranch, JIANGXING_GROUPS);
    const jiangxingByDay = findByThreeHarmony(dayBranch, JIANGXING_GROUPS);

    const found = [];
    bazi.branches.forEach((branch, i) => {
        if (branch === jiangxingByYear || branch === jiangxingByDay) {
            found.push({
                position: ['年支', '月支', '日支', '时支'][i],
                branch
            });
        }
    });

    return {
        name: '将星',
        description: '统领才能，适合管理',
        jiangxingBranches: [jiangxingByYear, jiangxingByDay].filter(Boolean),
        found,
        hasThis: found.length > 0
    };
}

/**
 * 综合神煞分析
 */
export function analyzeAllShensha(bazi) {
    const results = {
        tianyi: analyzeTianyiGuiren(bazi),
        wenchang: analyzeWenchang(bazi),
        yima: analyzeYima(bazi),
        taohua: analyzeTaohua(bazi),
        huagai: analyzeHuagai(bazi),
        yangren: analyzeYangren(bazi),
        jiangxing: analyzeJiangxing(bazi)
    };

    // 统计命中的神煞
    const activeShenshas = Object.values(results).filter(r => r.hasThis);

    return {
        ...results,
        summary: {
            total: activeShenshas.length,
            list: activeShenshas.map(r => r.name),
            auspicious: activeShenshas.filter(r =>
                ['天乙贵人', '文昌贵人', '将星'].includes(r.name)
            ).map(r => r.name),
            mixed: activeShenshas.filter(r =>
                ['驿马', '桃花', '华盖'].includes(r.name)
            ).map(r => r.name),
            inauspicious: activeShenshas.filter(r =>
                ['羊刃'].includes(r.name)
            ).map(r => r.name)
        }
    };
}
