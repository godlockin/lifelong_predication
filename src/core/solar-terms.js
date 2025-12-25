/**
 * 节气数据模块
 * 用于确定月柱的起始时间
 * 
 * 24节气中，有12个为"节"（用于定月柱）：
 * 立春、惊蛰、清明、立夏、芒种、小暑、立秋、白露、寒露、立冬、大雪、小寒
 */

// 节气名称
export const SOLAR_TERMS = [
    '小寒', '大寒', '立春', '雨水', '惊蛰', '春分',
    '清明', '谷雨', '立夏', '小满', '芒种', '夏至',
    '小暑', '大暑', '立秋', '处暑', '白露', '秋分',
    '寒露', '霜降', '立冬', '小雪', '大雪', '冬至'
];

// 月柱分界节气（12个"节"）
export const MONTH_BOUNDARY_TERMS = [
    '立春', '惊蛰', '清明', '立夏', '芒种', '小暑',
    '立秋', '白露', '寒露', '立冬', '大雪', '小寒'
];

// 节气对应的月份地支
export const TERM_TO_MONTH_BRANCH = {
    '立春': '寅', '惊蛰': '卯', '清明': '辰', '立夏': '巳',
    '芒种': '午', '小暑': '未', '立秋': '申', '白露': '酉',
    '寒露': '戌', '立冬': '亥', '大雪': '子', '小寒': '丑'
};

/**
 * 1989年精确节气数据 (月-日-时)
 */
const SOLAR_TERMS_1989 = [
    [1, 5, 16], [1, 20, 9], [2, 4, 4], [2, 18, 22], [3, 5, 16], [3, 20, 22],
    [4, 5, 3], [4, 20, 11], [5, 5, 20], [5, 21, 10], [6, 6, 1], [6, 21, 17],
    [7, 7, 11], [7, 23, 6], [8, 7, 23], [8, 23, 17], [9, 8, 4], [9, 23, 8],
    [10, 8, 15], [10, 23, 20], [11, 7, 21], [11, 22, 17], [12, 7, 7], [12, 22, 4]
];

/**
 * 精确节气数据表
 */
const SOLAR_TERMS_DATA = {
    1989: SOLAR_TERMS_1989
    // 可以继续添加其他年份
};

/**
 * 近似算法（用于没有精确数据的年份）
 * 基于改进的天文算法
 */
function calculateSolarTermApprox(year, termIndex) {
    const T = (year - 2000) / 100.0;
    // 春分点的儒略日
    const springEquinoxJD = 2451623.80984 + 365242.37404 * T + 0.05169 * T * T - 0.00411 * T * T * T;
    // 每个节气间隔
    const termInterval = 365.2422 / 24;
    // 春分是第5个节气（索引5）
    const jd = springEquinoxJD + (termIndex - 5) * termInterval;
    const milliseconds = (jd - 2440587.5) * 86400000;
    return new Date(milliseconds);
}

/**
 * 计算某年某节气的时间
 * 优先使用精确数据，否则使用近似算法
 * @param {number} year - 年份
 * @param {number} termIndex - 节气索引 (0-23)
 * @returns {Date} 节气时间
 */
export function calculateSolarTerm(year, termIndex) {
    const yearData = SOLAR_TERMS_DATA[year];
    if (yearData && yearData[termIndex]) {
        const [month, day, hour] = yearData[termIndex];
        return new Date(year, month - 1, day, hour, 0, 0);
    }
    return calculateSolarTermApprox(year, termIndex);
}

/**
 * 获取指定年份所有节气时间
 * @param {number} year - 年份
 * @returns {Array<{name: string, date: Date}>} 节气列表
 */
export function getYearSolarTerms(year) {
    return SOLAR_TERMS.map((name, index) => ({
        name,
        date: calculateSolarTerm(year, index)
    }));
}

/**
 * 根据日期判断当前所在的月柱地支
 * @param {Date} date - 真太阳时日期
 * @returns {{branch: string, termName: string}} 月支和分界节气
 */
export function getMonthBranch(date) {
    const year = date.getFullYear();
    const month = date.getMonth();

    // 获取当年和上一年的相关节气
    const currentYearTerms = getYearSolarTerms(year);
    const prevYearTerms = getYearSolarTerms(year - 1);

    // 构建月份分界节气时间表（从上一年大雪开始）
    const boundaries = [
        { name: '大雪', date: prevYearTerms[22].date, branch: '子' },
        { name: '小寒', date: currentYearTerms[0].date, branch: '丑' },
        { name: '立春', date: currentYearTerms[2].date, branch: '寅' },
        { name: '惊蛰', date: currentYearTerms[4].date, branch: '卯' },
        { name: '清明', date: currentYearTerms[6].date, branch: '辰' },
        { name: '立夏', date: currentYearTerms[8].date, branch: '巳' },
        { name: '芒种', date: currentYearTerms[10].date, branch: '午' },
        { name: '小暑', date: currentYearTerms[12].date, branch: '未' },
        { name: '立秋', date: currentYearTerms[14].date, branch: '申' },
        { name: '白露', date: currentYearTerms[16].date, branch: '酉' },
        { name: '寒露', date: currentYearTerms[18].date, branch: '戌' },
        { name: '立冬', date: currentYearTerms[20].date, branch: '亥' },
        { name: '大雪', date: currentYearTerms[22].date, branch: '子' }
    ];

    // 找到当前日期所在的月份
    for (let i = boundaries.length - 1; i >= 0; i--) {
        if (date >= boundaries[i].date) {
            return {
                branch: boundaries[i].branch,
                termName: boundaries[i].name
            };
        }
    }

    // 默认返回丑月（小寒之前）
    return { branch: '丑', termName: '小寒' };
}

/**
 * 判断日期是否在立春之后（用于年柱判定）
 * @param {Date} date - 日期
 * @returns {boolean} 是否在立春之后
 */
export function isAfterLichun(date) {
    const year = date.getFullYear();
    const lichun = calculateSolarTerm(year, 2); // 立春是第3个节气（索引2）
    return date >= lichun;
}

/**
 * 获取用于年柱计算的年份
 * 如果在立春之前，使用上一年
 * @param {Date} date - 日期
 * @returns {number} 干支年份
 */
export function getGanzhiYear(date) {
    const year = date.getFullYear();
    return isAfterLichun(date) ? year : year - 1;
}
