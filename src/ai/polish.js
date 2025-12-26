/**
 * AI润色服务模块
 * 
 * 使用 Google Gemini 2.0 Flash 模型
 * SDK: @google/genai (新版统一SDK)
 */

import { getPrompt } from './prompts.js';

// 默认模型
const DEFAULT_MODEL = 'gemini-2.0-flash';

/**
 * 创建 Gemini 客户端
 * @param {string} apiKey - API密钥
 * @returns {Object} 客户端实例
 */
async function createGeminiClient(apiKey) {
    const { GoogleGenAI } = await import('@google/genai');
    return new GoogleGenAI({ apiKey });
}

/**
 * 使用 Gemini 进行文本生成
 * @param {string} prompt - 提示词
 * @param {string} apiKey - API密钥
 * @param {Object} options - 选项
 * @returns {Promise<string>} 生成的文本
 */
export async function generateWithGemini(prompt, apiKey, options = {}) {
    const {
        model = DEFAULT_MODEL,
        temperature = 0.7,
        maxTokens = 2048
    } = options;

    try {
        const genai = await createGeminiClient(apiKey);

        const response = await genai.models.generateContent({
            model,
            contents: prompt,
            config: {
                temperature,
                maxOutputTokens: maxTokens
            }
        });

        return response.text || '';
    } catch (error) {
        console.error('Gemini API Error:', error);
        throw new Error(`AI润色失败: ${error.message}`);
    }
}

/**
 * 使用流式输出生成（可选）
 * @param {string} prompt - 提示词
 * @param {string} apiKey - API密钥
 * @param {Function} onChunk - 每个chunk的回调
 * @returns {Promise<string>} 完整响应
 */
export async function generateStreamWithGemini(prompt, apiKey, onChunk) {
    const genai = await createGeminiClient(apiKey);

    const response = await genai.models.generateContentStream({
        model: DEFAULT_MODEL,
        contents: prompt
    });

    let fullText = '';
    for await (const chunk of response) {
        const text = chunk.text || '';
        fullText += text;
        if (onChunk) {
            onChunk(text);
        }
    }

    return fullText;
}

/**
 * 润色命理分析报告
 * @param {Object} analysisData - 分析数据
 * @param {Object} options - 选项
 * @returns {Promise<Object>} 润色后的报告
 */
export async function polishReport(analysisData, options = {}) {
    const {
        apiKey,
        type = 'comprehensive',
        tone = 'professional',
        model = DEFAULT_MODEL
    } = options;

    if (!apiKey) {
        return {
            success: false,
            error: '缺少API密钥'
        };
    }

    try {
        const prompt = getPrompt(type, analysisData, tone);
        const polishedText = await generateWithGemini(prompt, apiKey, { model });

        return {
            success: true,
            polished: polishedText,
            model,
            type,
            tone
        };
    } catch (error) {
        return {
            success: false,
            error: error.message
        };
    }
}

/**
 * 批量润色多个部分
 * @param {Object} sections - 各部分数据
 * @param {string} apiKey - API密钥
 * @returns {Promise<Object>} 润色结果
 */
export async function polishMultipleSections(sections, apiKey) {
    const results = {};

    for (const [key, data] of Object.entries(sections)) {
        try {
            const prompt = getPrompt(key, data);
            results[key] = await generateWithGemini(prompt, apiKey);
        } catch (error) {
            results[key] = { error: error.message };
        }
    }

    return results;
}

/**
 * 创建简化版润色（不需要API,使用模板）
 * @param {Object} analysisData - 分析数据
 * @returns {Object} 模板化报告
 */
export function createTemplateReport(analysisData) {
    const { bazi, tenGods, fiveElements, derivatives } = analysisData;
    const { shensha, nayin, relations, kongwang } = derivatives || {};

    let report = [];

    // 八字基本信息
    if (bazi) {
        report.push(`【八字命盘】${bazi.pillars || '未知'}`);
        report.push(`日主：${bazi.dayMaster || '未知'}`);
    }

    // 五行分析
    if (fiveElements) {
        report.push(`\n【五行分析】`);
        report.push(`日主五行：${fiveElements.dayElement}`);
        const strengthDesc = fiveElements.strength === '旺' ? '身旺' :
            fiveElements.strength === '弱' ? '身弱' : '中和';
        report.push(`命主${strengthDesc}`);

        if (fiveElements.distribution) {
            const distStr = Object.entries(fiveElements.distribution)
                .map(([e, p]) => `${e}:${p}%`)
                .join(' ');
            report.push(`五行分布：${distStr}`);
        }

        if (fiveElements.preference) {
            report.push(`\n喜用神：${fiveElements.preference.favorable.join('、')}`);
            report.push(`忌神：${fiveElements.preference.unfavorable.join('、')}`);
        }
    }

    // 十神分析
    if (tenGods) {
        report.push(`\n【十神分析】`);
        if (tenGods.stemGods) {
            report.push(`年干：${tenGods.stemGods.year || '无'}`);
            report.push(`月干：${tenGods.stemGods.month || '无'}`);
            report.push(`时干：${tenGods.stemGods.hour || '无'}`);
        }
        if (tenGods.godCount) {
            const counts = Object.entries(tenGods.godCount)
                .filter(([_, count]) => count > 0)
                .map(([god, count]) => `${god}×${count}`)
                .join('、');
            if (counts) {
                report.push(`十神分布：${counts}`);
            }
        }
    }

    // 神煞
    if (shensha?.summary) {
        report.push(`\n【神煞分析】`);
        if (shensha.summary.auspicious.length > 0) {
            report.push(`吉神：${shensha.summary.auspicious.join('、')}`);
        }
        if (shensha.summary.mixed.length > 0) {
            report.push(`中性神煞：${shensha.summary.mixed.join('、')}`);
        }
        if (shensha.summary.inauspicious.length > 0) {
            report.push(`凶煞：${shensha.summary.inauspicious.join('、')}`);
        }
    }

    // 纳音
    if (nayin) {
        report.push(`\n【纳音命理】`);
        report.push(`日柱纳音：${nayin.mainNayin}`);
        report.push(`纳音五行：${nayin.mainElement}`);
        if (nayin.summary) {
            report.push(nayin.summary);
        }
    }

    // 空亡
    if (kongwang) {
        report.push(`\n【空亡】`);
        report.push(kongwang.summary || '无空亡');
    }

    // 刑冲合害
    if (relations?.summary) {
        report.push(`\n【干支关系】`);
        if (relations.summary.combines.length > 0) {
            report.push(`合：${relations.summary.combines.map(c => c.description).join('；')}`);
        }
        if (relations.summary.conflicts.length > 0) {
            report.push(`冲/刑/害：${relations.summary.conflicts.map(c => c.description).join('；')}`);
        }
        if (relations.summary.combines.length === 0 && relations.summary.conflicts.length === 0) {
            report.push('干支平和，无明显刑冲合害');
        }
    }

    // 紫微斗数
    if (analysisData.ziwei && analysisData.ziwei.available) {
        const z = analysisData.ziwei;
        report.push(`\n【紫微斗数】`);
        report.push(`格局：${z.basicInfo.fiveElementsClass} · 命主${z.basicInfo.soul} · 身主${z.basicInfo.body}`);
        
        if (z.analysis) {
            if (z.analysis.ming) {
                const stars = z.analysis.ming.stars.length > 0 ? z.analysis.ming.stars.join('、') : '无主星';
                report.push(`命宫：${stars} (${z.analysis.ming.interpretation})`);
            }
            if (z.analysis.marriage) {
                const stars = z.analysis.marriage.stars.length > 0 ? z.analysis.marriage.stars.join('、') : '无主星';
                report.push(`夫妻宫：${stars}`);
            }
            if (z.analysis.career) {
                const stars = z.analysis.career.stars.length > 0 ? z.analysis.career.stars.join('、') : '无主星';
                report.push(`事业宫：${stars}`);
            }
            if (z.analysis.wealth) {
                const stars = z.analysis.wealth.stars.length > 0 ? z.analysis.wealth.stars.join('、') : '无主星';
                report.push(`财帛宫：${stars}`);
            }
        }
    }

    return {
        success: true,
        polished: report.join('\n'),
        isTemplate: true,
        note: '此为模板化报告，如需AI润色请配置GEMINI_API_KEY'
    };
}

