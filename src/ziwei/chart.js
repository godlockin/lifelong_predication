/**
 * 紫微斗数命盘排盘模块
 * 
 * 封装 iztro 库进行排盘
 */

// 注意：实际部署时需要安装 iztro 包
// npm install iztro

/**
 * 生成紫微斗数命盘
 * @param {string} solarDate - 公历日期 YYYY-MM-DD
 * @param {number} hour - 时辰（0-23）
 * @param {string} gender - 性别 '男' 或 '女'
 * @returns {Object} 命盘数据
 */
export async function generateZiweiChart(solarDate, hour, gender) {
    try {
        // 动态导入 iztro（支持 tree-shaking）
        const { astro } = await import('iztro');

        // 时辰转换（0-23小时转为时辰索引0-11）
        const hourIndex = getHourIndex(hour);

        // 生成命盘
        const chart = astro.bySolar(solarDate, hourIndex, gender === '女' ? '女' : '男');

        return {
            success: true,
            chart,
            // 提取关键信息
            summary: extractChartSummary(chart)
        };
    } catch (error) {
        return {
            success: false,
            error: error.message,
            // 提供简化版分析
            summary: generateSimplifiedAnalysis(solarDate, hour, gender)
        };
    }
}

/**
 * 将小时转换为时辰索引
 * @param {number} hour - 0-23
 * @returns {number} 0-11
 */
function getHourIndex(hour) {
    if (hour >= 23 || hour < 1) return 0;  // 子时
    if (hour < 3) return 1;   // 丑时
    if (hour < 5) return 2;   // 寅时
    if (hour < 7) return 3;   // 卯时
    if (hour < 9) return 4;   // 辰时
    if (hour < 11) return 5;  // 巳时
    if (hour < 13) return 6;  // 午时
    if (hour < 15) return 7;  // 未时
    if (hour < 17) return 8;  // 申时
    if (hour < 19) return 9;  // 酉时
    if (hour < 21) return 10; // 戌时
    return 11; // 亥时
}

/**
 * 提取命盘摘要
 * @param {Object} chart - iztro 命盘对象
 * @returns {Object} 摘要信息
 */
function extractChartSummary(chart) {
    if (!chart) return null;

    try {
        return {
            // 基本信息
            solarDate: chart.solarDate,
            lunarDate: chart.lunarDate,
            gender: chart.gender,

            // 命主和身主
            soul: chart.soul,
            body: chart.body,

            // 五行局
            fiveElementsClass: chart.fiveElementsClass,

            // 十二宫位
            palaces: chart.palaces?.map(palace => ({
                name: palace.name,
                heavenlyStem: palace.heavenlyStem,
                earthlyBranch: palace.earthlyBranch,
                majorStars: palace.majorStars?.map(s => s.name) || [],
                minorStars: palace.minorStars?.map(s => s.name) || [],
                // 命宫主星
                isMainPalace: palace.name === '命宫'
            })) || [],

            // 大限信息
            decadalFate: chart.decadalFate
        };
    } catch (e) {
        return null;
    }
}

/**
 * 简化版紫微分析（当iztro不可用时）
 * @param {string} solarDate - 日期
 * @param {number} hour - 时辰
 * @param {string} gender - 性别
 * @returns {Object} 简化分析
 */
function generateSimplifiedAnalysis(solarDate, hour, gender) {
    return {
        note: '紫微斗数需要安装iztro库进行完整排盘',
        solarDate,
        hour,
        gender,
        recommendation: '请运行 npm install iztro 安装紫微斗数排盘库'
    };
}

/**
 * 十二宫位名称
 */
export const TWELVE_PALACES = [
    '命宫', '兄弟宫', '夫妻宫', '子女宫',
    '财帛宫', '疾厄宫', '迁移宫', '交友宫',
    '事业宫', '田宅宫', '福德宫', '父母宫'
];

/**
 * 宫位含义
 */
export const PALACE_MEANINGS = {
    '命宫': '代表命主本人的性格、才能、一生格局',
    '兄弟宫': '代表兄弟姐妹、同事、朋友关系',
    '夫妻宫': '代表婚姻、感情、配偶状况',
    '子女宫': '代表子女缘分、与晚辈关系',
    '财帛宫': '代表财运、理财能力、收入状况',
    '疾厄宫': '代表健康状况、易患疾病',
    '迁移宫': '代表外出运、变动、贵人运',
    '交友宫': '代表人际关系、社交能力',
    '事业宫': '代表事业发展、工作状况',
    '田宅宫': '代表不动产、家庭环境',
    '福德宫': '代表精神生活、兴趣爱好',
    '父母宫': '代表与父母长辈关系、家族背景'
};
