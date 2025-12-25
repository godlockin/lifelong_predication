/**
 * 八字排盘核心引擎
 * 
 * 四柱：年柱、月柱、日柱、时柱
 * 每柱由一个天干和一个地支组成
 */

import { HEAVENLY_STEMS, getStemByIndex } from './heavenly-stems.js';
import { EARTHLY_BRANCHES, getBranchByIndex, getBranchByHour } from './earthly-branches.js';
import { getMonthBranch, getGanzhiYear, isAfterLichun } from './solar-terms.js';
import { calculateTrueSolarTime } from './solar-time.js';

// 六十甲子表
export const SIXTY_JIAZI = (() => {
    const jiazi = [];
    for (let i = 0; i < 60; i++) {
        jiazi.push({
            stem: HEAVENLY_STEMS[i % 10],
            branch: EARTHLY_BRANCHES[i % 12],
            ganzhi: HEAVENLY_STEMS[i % 10] + EARTHLY_BRANCHES[i % 12]
        });
    }
    return jiazi;
})();

/**
 * 五虎遁年起月表
 * 根据年干确定正月（寅月）的天干
 */
const YEAR_STEM_TO_MONTH_STEM = {
    '甲': '丙', '己': '丙', // 甲己之年丙作首
    '乙': '戊', '庚': '戊', // 乙庚之年戊为头
    '丙': '庚', '辛': '庚', // 丙辛之岁寻庚上
    '丁': '壬', '壬': '壬', // 丁壬壬位顺行流
    '戊': '甲', '癸': '甲'  // 戊癸何方发，甲正好追求
};

/**
 * 五鼠遁日起时表
 * 根据日干确定子时的天干
 */
const DAY_STEM_TO_HOUR_STEM = {
    '甲': '甲', '己': '甲', // 甲己还加甲
    '乙': '丙', '庚': '丙', // 乙庚丙作初
    '丙': '戊', '辛': '戊', // 丙辛从戊起
    '丁': '庚', '壬': '庚', // 丁壬庚子居
    '戊': '壬', '癸': '壬'  // 戊癸何方发，壬子是真途
};

/**
 * 计算年柱
 * 以立春为分界
 * @param {Date} date - 真太阳时
 * @returns {{stem: string, branch: string, ganzhi: string}}
 */
export function calculateYearPillar(date) {
    const year = getGanzhiYear(date);

    // 天干：(年份 - 4) % 10
    // 公元4年为甲子年
    const stemIndex = (year - 4) % 10;
    const stem = getStemByIndex(stemIndex);

    // 地支：(年份 - 4) % 12
    const branchIndex = (year - 4) % 12;
    const branch = getBranchByIndex(branchIndex);

    return { stem, branch, ganzhi: stem + branch };
}

/**
 * 计算月柱
 * 根据节气确定月支，根据年干确定月干
 * @param {Date} date - 真太阳时
 * @param {string} yearStem - 年干
 * @returns {{stem: string, branch: string, ganzhi: string}}
 */
export function calculateMonthPillar(date, yearStem) {
    // 获取月支
    const { branch } = getMonthBranch(date);

    // 月支索引（寅=0, 卯=1, ..., 丑=11）
    const branchOrder = ['寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥', '子', '丑'];
    const monthIndex = branchOrder.indexOf(branch);

    // 根据年干查找正月（寅月）的天干
    const firstMonthStem = YEAR_STEM_TO_MONTH_STEM[yearStem];
    const firstMonthStemIndex = HEAVENLY_STEMS.indexOf(firstMonthStem);

    // 计算当月天干
    const stemIndex = (firstMonthStemIndex + monthIndex) % 10;
    const stem = getStemByIndex(stemIndex);

    return { stem, branch, ganzhi: stem + branch };
}

/**
 * 计算日柱
 * 基于基准日期计算
 * @param {Date} date - 真太阳时
 * @returns {{stem: string, branch: string, ganzhi: string}}
 */
export function calculateDayPillar(date) {
    // 基准日期：1900年1月31日为甲辰日
    // 甲辰在六十甲子中是第40位（索引40）
    const baseDate = new Date(1900, 0, 31);
    const baseJiaziIndex = 40;

    // 计算日期差
    const dayDiff = Math.floor((date - baseDate) / (24 * 60 * 60 * 1000));

    // 计算六十甲子索引
    const jiaziIndex = ((baseJiaziIndex + dayDiff) % 60 + 60) % 60;

    return SIXTY_JIAZI[jiaziIndex];
}

/**
 * 计算时柱
 * 根据时辰确定时支，根据日干确定时干
 * 注意：时柱使用原始本地时间，不进行真太阳时修正
 * @param {Date} localDate - 本地时间（未修正）
 * @param {string} dayStem - 日干
 * @returns {{stem: string, branch: string, ganzhi: string}}
 */
export function calculateHourPillar(localDate, dayStem) {
    const hour = localDate.getHours();
    const minute = localDate.getMinutes();

    // 获取时支（传入分钟以处理整点边界）
    const branch = getBranchByHour(hour, minute);

    // 时支索引
    const branchIndex = EARTHLY_BRANCHES.indexOf(branch);

    // 根据日干查找子时的天干
    const ziHourStem = DAY_STEM_TO_HOUR_STEM[dayStem];
    const ziHourStemIndex = HEAVENLY_STEMS.indexOf(ziHourStem);

    // 计算当前时辰天干
    const stemIndex = (ziHourStemIndex + branchIndex) % 10;
    const stem = getStemByIndex(stemIndex);

    return { stem, branch, ganzhi: stem + branch };
}

/**
 * 完整八字排盘
 * @param {Date} date - 出生时间（当地标准时间）
 * @param {number} longitude - 出生地经度
 * @param {number} timezone - 时区（默认8）
 * @returns {Object} 八字信息
 */
export function calculateBazi(date, longitude, timezone = 8) {
    // 计算真太阳时
    const trueSolarTime = calculateTrueSolarTime(date, longitude, timezone);

    // 计算四柱
    // 年月日柱使用真太阳时
    const yearPillar = calculateYearPillar(trueSolarTime);
    const monthPillar = calculateMonthPillar(trueSolarTime, yearPillar.stem);
    const dayPillar = calculateDayPillar(trueSolarTime);
    // 时柱使用原始本地时间（不进行真太阳时修正）
    const hourPillar = calculateHourPillar(date, dayPillar.stem);

    return {
        // 时间信息
        originalTime: date,
        trueSolarTime,
        longitude,
        timezone,

        // 四柱
        yearPillar,
        monthPillar,
        dayPillar,
        hourPillar,

        // 八字字符串
        bazi: `${yearPillar.ganzhi} ${monthPillar.ganzhi} ${dayPillar.ganzhi} ${hourPillar.ganzhi}`,

        // 日主（日干）
        dayMaster: dayPillar.stem,

        // 四柱数组（便于遍历）
        pillars: [yearPillar, monthPillar, dayPillar, hourPillar],

        // 所有天干
        stems: [yearPillar.stem, monthPillar.stem, dayPillar.stem, hourPillar.stem],

        // 所有地支
        branches: [yearPillar.branch, monthPillar.branch, dayPillar.branch, hourPillar.branch]
    };
}

/**
 * 简化版八字排盘（不需要经度，使用标准时间）
 * @param {Date} date - 出生时间
 * @returns {Object} 八字信息
 */
export function calculateBaziSimple(date) {
    // 使用东八区标准经度
    return calculateBazi(date, 120, 8);
}
