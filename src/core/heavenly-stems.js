/**
 * 天干数据模块
 * 十天干：甲乙丙丁戊己庚辛壬癸
 */

// 天干列表
export const HEAVENLY_STEMS = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸'];

// 天干索引映射
export const STEM_INDEX = Object.fromEntries(HEAVENLY_STEMS.map((s, i) => [s, i]));

// 天干五行
export const STEM_ELEMENT = {
  '甲': '木', '乙': '木',
  '丙': '火', '丁': '火',
  '戊': '土', '己': '土',
  '庚': '金', '辛': '金',
  '壬': '水', '癸': '水'
};

// 天干阴阳
export const STEM_POLARITY = {
  '甲': '阳', '乙': '阴',
  '丙': '阳', '丁': '阴',
  '戊': '阳', '己': '阴',
  '庚': '阳', '辛': '阴',
  '壬': '阳', '癸': '阴'
};

// 天干五合
export const STEM_COMBINE = {
  '甲': '己', '己': '甲', // 甲己合土
  '乙': '庚', '庚': '乙', // 乙庚合金
  '丙': '辛', '辛': '丙', // 丙辛合水
  '丁': '壬', '壬': '丁', // 丁壬合木
  '戊': '癸', '癸': '戊'  // 戊癸合火
};

// 天干五合化气
export const STEM_COMBINE_RESULT = {
  '甲己': '土', '乙庚': '金', '丙辛': '水', '丁壬': '木', '戊癸': '火'
};

// 天干相冲（隔五位）
export const STEM_CLASH = {
  '甲': '庚', '庚': '甲',
  '乙': '辛', '辛': '乙',
  '丙': '壬', '壬': '丙',
  '丁': '癸', '癸': '丁'
  // 戊己土居中央，无冲
};

/**
 * 获取天干索引
 */
export function getStemIndex(stem) {
  return STEM_INDEX[stem];
}

/**
 * 根据索引获取天干
 */
export function getStemByIndex(index) {
  return HEAVENLY_STEMS[((index % 10) + 10) % 10];
}

/**
 * 获取天干五行
 */
export function getStemElement(stem) {
  return STEM_ELEMENT[stem];
}

/**
 * 判断天干阴阳
 */
export function isStemYang(stem) {
  return STEM_POLARITY[stem] === '阳';
}

/**
 * 检查两天干是否相合
 */
export function checkStemCombine(stem1, stem2) {
  return STEM_COMBINE[stem1] === stem2;
}

/**
 * 检查两天干是否相冲
 */
export function checkStemClash(stem1, stem2) {
  return STEM_CLASH[stem1] === stem2;
}
