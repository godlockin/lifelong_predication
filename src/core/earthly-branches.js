/**
 * 地支数据模块
 * 十二地支：子丑寅卯辰巳午未申酉戌亥
 */

// 地支列表
export const EARTHLY_BRANCHES = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥'];

// 地支索引映射
export const BRANCH_INDEX = Object.fromEntries(EARTHLY_BRANCHES.map((b, i) => [b, i]));

// 地支五行
export const BRANCH_ELEMENT = {
    '子': '水', '丑': '土', '寅': '木', '卯': '木',
    '辰': '土', '巳': '火', '午': '火', '未': '土',
    '申': '金', '酉': '金', '戌': '土', '亥': '水'
};

// 地支阴阳
export const BRANCH_POLARITY = {
    '子': '阳', '丑': '阴', '寅': '阳', '卯': '阴',
    '辰': '阳', '巳': '阴', '午': '阳', '未': '阴',
    '申': '阳', '酉': '阴', '戌': '阳', '亥': '阴'
};

// 地支藏干 [本气, 中气, 余气]
export const BRANCH_HIDDEN_STEMS = {
    '子': ['癸'],
    '丑': ['己', '癸', '辛'],
    '寅': ['甲', '丙', '戊'],
    '卯': ['乙'],
    '辰': ['戊', '乙', '癸'],
    '巳': ['丙', '庚', '戊'],
    '午': ['丁', '己'],
    '未': ['己', '丁', '乙'],
    '申': ['庚', '壬', '戊'],
    '酉': ['辛'],
    '戌': ['戊', '辛', '丁'],
    '亥': ['壬', '甲']
};

// 地支六合
export const BRANCH_SIX_COMBINE = {
    '子': '丑', '丑': '子', // 子丑合土
    '寅': '亥', '亥': '寅', // 寅亥合木
    '卯': '戌', '戌': '卯', // 卯戌合火
    '辰': '酉', '酉': '辰', // 辰酉合金
    '巳': '申', '申': '巳', // 巳申合水
    '午': '未', '未': '午'  // 午未合火
};

// 地支六合化气
export const BRANCH_SIX_COMBINE_RESULT = {
    '子丑': '土', '寅亥': '木', '卯戌': '火',
    '辰酉': '金', '巳申': '水', '午未': '火'
};

// 地支三合
export const BRANCH_THREE_COMBINE = {
    '申子辰': '水', // 水局
    '亥卯未': '木', // 木局
    '寅午戌': '火', // 火局
    '巳酉丑': '金'  // 金局
};

// 地支三合成员
export const BRANCH_THREE_COMBINE_GROUPS = [
    ['申', '子', '辰'], // 水局
    ['亥', '卯', '未'], // 木局
    ['寅', '午', '戌'], // 火局
    ['巳', '酉', '丑']  // 金局
];

// 地支六冲
export const BRANCH_SIX_CLASH = {
    '子': '午', '午': '子',
    '丑': '未', '未': '丑',
    '寅': '申', '申': '寅',
    '卯': '酉', '酉': '卯',
    '辰': '戌', '戌': '辰',
    '巳': '亥', '亥': '巳'
};

// 地支三刑
export const BRANCH_THREE_PUNISHMENT = {
    // 无礼之刑
    '子': '卯', '卯': '子',
    // 无恩之刑
    '寅': '巳', '巳': '申', '申': '寅',
    // 恃势之刑
    '丑': '戌', '戌': '未', '未': '丑',
    // 自刑
    '辰': '辰', '午': '午', '酉': '酉', '亥': '亥'
};

// 地支相害
export const BRANCH_HARM = {
    '子': '未', '未': '子',
    '丑': '午', '午': '丑',
    '寅': '巳', '巳': '寅',
    '卯': '辰', '辰': '卯',
    '申': '亥', '亥': '申',
    '酉': '戌', '戌': '酉'
};

// 时辰对应小时范围
export const BRANCH_HOUR_RANGE = {
    '子': [23, 1],  // 23:00 - 00:59
    '丑': [1, 3],   // 01:00 - 02:59
    '寅': [3, 5],
    '卯': [5, 7],
    '辰': [7, 9],
    '巳': [9, 11],
    '午': [11, 13],
    '未': [13, 15],
    '申': [15, 17],
    '酉': [17, 19],
    '戌': [19, 21],
    '亥': [21, 23]
};

/**
 * 获取地支索引
 */
export function getBranchIndex(branch) {
    return BRANCH_INDEX[branch];
}

/**
 * 根据索引获取地支
 */
export function getBranchByIndex(index) {
    return EARTHLY_BRANCHES[((index % 12) + 12) % 12];
}

/**
 * 获取地支五行
 */
export function getBranchElement(branch) {
    return BRANCH_ELEMENT[branch];
}

/**
 * 获取地支藏干
 */
export function getHiddenStems(branch) {
    return BRANCH_HIDDEN_STEMS[branch] || [];
}

/**
 * 根据小时和分钟获取时辰地支
 * 规则：整点算前一时辰，过了整点则算下一时辰
 * 例如：1:00算子时，1:01算丑时；13:00算午时，13:01算未时
 * @param {number} hour - 小时 (0-23)
 * @param {number} minute - 分钟 (0-59)
 * @returns {string} 时辰地支
 */
export function getBranchByHour(hour, minute = 0) {
    // 子时特殊处理：23:00-23:59 和 0:00-1:00
    if (hour === 23 || hour === 0) return '子';
    if (hour === 1 && minute === 0) return '子';  // 1:00整点算子时
    if (hour === 1) return '丑';  // 1:01开始算丑时

    // 其他时辰：整点算前一时辰，过了整点算当前时辰
    if (hour === 3 && minute === 0) return '丑';
    if (hour >= 3 && hour < 5) return '寅';
    if (hour === 5 && minute === 0) return '寅';
    if (hour >= 5 && hour < 7) return '卯';
    if (hour === 7 && minute === 0) return '卯';
    if (hour >= 7 && hour < 9) return '辰';
    if (hour === 9 && minute === 0) return '辰';
    if (hour >= 9 && hour < 11) return '巳';
    if (hour === 11 && minute === 0) return '巳';
    if (hour >= 11 && hour < 13) return '午';
    if (hour === 13 && minute === 0) return '午';
    if (hour >= 13 && hour < 15) return '未';
    if (hour === 15 && minute === 0) return '未';
    if (hour >= 15 && hour < 17) return '申';
    if (hour === 17 && minute === 0) return '申';
    if (hour >= 17 && hour < 19) return '酉';
    if (hour === 19 && minute === 0) return '酉';
    if (hour >= 19 && hour < 21) return '戌';
    if (hour === 21 && minute === 0) return '戌';
    if (hour >= 21 && hour < 23) return '亥';

    // 默认（不应到达）
    return '子';
}

/**
 * 检查两地支是否六合
 */
export function checkBranchCombine(branch1, branch2) {
    return BRANCH_SIX_COMBINE[branch1] === branch2;
}

/**
 * 检查两地支是否六冲
 */
export function checkBranchClash(branch1, branch2) {
    return BRANCH_SIX_CLASH[branch1] === branch2;
}

/**
 * 检查是否构成三合局
 */
export function checkThreeCombine(branches) {
    const set = new Set(branches);
    for (const group of BRANCH_THREE_COMBINE_GROUPS) {
        if (group.every(b => set.has(b))) {
            return group.join('');
        }
    }
    return null;
}
