/**
 * 功能测试脚本
 */

import { calculateBazi } from './src/core/bazi.js';
import { calculateTrueSolarTime, getSolarTimeDetails } from './src/core/solar-time.js';
import { analyzeTenGods } from './src/analysis/ten-gods.js';
import { analyzeDayMasterStrength } from './src/analysis/five-elements.js';
import { analyzeAllShensha } from './src/derivatives/shensha.js';
import { analyzeNayin } from './src/derivatives/nayin.js';
import { analyzeKongwang } from './src/derivatives/kongwang.js';
import { analyzeRelations } from './src/derivatives/relations.js';
import { performQuickAnalysis } from './src/schools/comprehensive.js';

console.log('='.repeat(60));
console.log('命理测算系统功能测试');
console.log('='.repeat(60));

// 测试案例：1990年8月15日 14:30，北京
const testDate = new Date(1990, 7, 15, 14, 30); // 月份从0开始
const longitude = 116.4074; // 北京经度

console.log('\n【测试输入】');
console.log(`出生时间: ${testDate.toLocaleString()}`);
console.log(`出生地点: 北京 (经度 ${longitude}°)`);

// 1. 真太阳时测试
console.log('\n【真太阳时计算】');
const solarDetails = getSolarTimeDetails(testDate, longitude);
console.log(`标准时间: ${testDate.toLocaleString()}`);
console.log(`真太阳时: ${solarDetails.trueSolarTime.toLocaleString()}`);
console.log(`经度校正: ${solarDetails.longitudeCorrection} 分钟`);
console.log(`均时差: ${solarDetails.equationOfTime} 分钟`);
console.log(`总校正: ${solarDetails.totalCorrection} 分钟`);

// 2. 八字排盘测试
console.log('\n【八字排盘】');
const bazi = calculateBazi(testDate, longitude);
console.log(`八字: ${bazi.bazi}`);
console.log(`年柱: ${bazi.yearPillar.ganzhi}`);
console.log(`月柱: ${bazi.monthPillar.ganzhi}`);
console.log(`日柱: ${bazi.dayPillar.ganzhi}`);
console.log(`时柱: ${bazi.hourPillar.ganzhi}`);
console.log(`日主: ${bazi.dayMaster}`);

// 3. 十神分析
console.log('\n【十神分析】');
const tenGods = analyzeTenGods(bazi);
console.log(`年干十神: ${tenGods.stemGods.year}`);
console.log(`月干十神: ${tenGods.stemGods.month}`);
console.log(`时干十神: ${tenGods.stemGods.hour}`);
console.log(`十神统计:`, tenGods.godCount);

// 4. 五行旺衰
console.log('\n【五行分析】');
const fiveElements = analyzeDayMasterStrength(bazi);
console.log(`日主五行: ${fiveElements.dayElement}`);
console.log(`日主强弱: ${fiveElements.strength}`);
console.log(`五行分布:`, fiveElements.distribution);

// 5. 神煞分析
console.log('\n【神煞分析】');
const shensha = analyzeAllShensha(bazi);
console.log(`命中神煞: ${shensha.summary.list.join('、') || '无'}`);
if (shensha.summary.auspicious.length > 0) {
    console.log(`吉神: ${shensha.summary.auspicious.join('、')}`);
}

// 6. 纳音分析
console.log('\n【纳音分析】');
const nayin = analyzeNayin(bazi);
console.log(`日柱纳音: ${nayin.mainNayin}`);
console.log(`纳音五行: ${nayin.mainElement}`);

// 7. 空亡分析
console.log('\n【空亡分析】');
const kongwang = analyzeKongwang(bazi);
console.log(kongwang.summary);

// 8. 刑冲合害
console.log('\n【刑冲合害】');
const relations = analyzeRelations(bazi);
if (relations.summary.combines.length > 0) {
    console.log(`合: ${relations.summary.combines.map(c => c.description).join('、')}`);
}
if (relations.summary.conflicts.length > 0) {
    console.log(`冲/刑/害: ${relations.summary.conflicts.map(c => c.description).join('、')}`);
}

// 9. 快速分析
console.log('\n【快速分析汇总】');
const quick = performQuickAnalysis({ birthDate: testDate, longitude });
console.log(quick);

console.log('\n' + '='.repeat(60));
console.log('✅ 所有功能测试完成！');
console.log('='.repeat(60));
