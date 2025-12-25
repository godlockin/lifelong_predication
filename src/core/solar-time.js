/**
 * 真太阳时计算模块
 * 
 * 真太阳时 = 当地标准时间 + 经度时差 + 均时差
 */

/**
 * 计算均时差 (Equation of Time)
 * @param {Date} date - 日期
 * @returns {number} 均时差（分钟）
 */
export function calculateEquationOfTime(date) {
    const year = date.getFullYear();
    const start = new Date(year, 0, 1);
    const dayOfYear = Math.floor((date - start) / (24 * 60 * 60 * 1000)) + 1;

    // B = 360° × (d - 81) / 365
    const B = (360 * (dayOfYear - 81) / 365) * (Math.PI / 180);

    // EoT ≈ 9.87×sin(2B) - 7.53×cos(B) - 1.5×sin(B)
    const eot = 9.87 * Math.sin(2 * B) - 7.53 * Math.cos(B) - 1.5 * Math.sin(B);

    return eot; // 分钟
}

/**
 * 计算经度时差
 * @param {number} longitude - 当地经度
 * @param {number} timezone - 时区（默认东八区）
 * @returns {number} 经度时差（分钟）
 */
export function calculateLongitudeCorrection(longitude, timezone = 8) {
    // 时区标准经度 = 时区 × 15°
    const standardLongitude = timezone * 15;
    // 经度时差 = (经度 - 标准经度) × 4分钟/度
    return (longitude - standardLongitude) * 4;
}

/**
 * 计算真太阳时
 * @param {Date} date - 当地标准时间
 * @param {number} longitude - 当地经度
 * @param {number} timezone - 时区（默认8，东八区）
 * @returns {Date} 真太阳时
 */
export function calculateTrueSolarTime(date, longitude, timezone = 8) {
    const longitudeCorrection = calculateLongitudeCorrection(longitude, timezone);
    const equationOfTime = calculateEquationOfTime(date);

    // 总校正量（分钟）
    const totalCorrection = longitudeCorrection + equationOfTime;

    // 创建新的日期对象，加上校正量
    const trueSolarTime = new Date(date.getTime() + totalCorrection * 60 * 1000);

    return trueSolarTime;
}

/**
 * 获取真太阳时的时辰
 * @param {Date} trueSolarTime - 真太阳时
 * @returns {number} 小时数 (0-23)
 */
export function getTrueSolarHour(trueSolarTime) {
    return trueSolarTime.getHours() + trueSolarTime.getMinutes() / 60;
}

/**
 * 格式化时间校正信息
 * @param {Date} date - 原始时间
 * @param {number} longitude - 经度
 * @param {number} timezone - 时区
 * @returns {Object} 校正详情
 */
export function getSolarTimeDetails(date, longitude, timezone = 8) {
    const longitudeCorrection = calculateLongitudeCorrection(longitude, timezone);
    const equationOfTime = calculateEquationOfTime(date);
    const trueSolarTime = calculateTrueSolarTime(date, longitude, timezone);

    return {
        originalTime: date,
        trueSolarTime,
        longitude,
        timezone,
        standardLongitude: timezone * 15,
        longitudeCorrection: Math.round(longitudeCorrection * 10) / 10, // 保留一位小数
        equationOfTime: Math.round(equationOfTime * 10) / 10,
        totalCorrection: Math.round((longitudeCorrection + equationOfTime) * 10) / 10
    };
}
