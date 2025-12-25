/**
 * 城市经纬度数据
 * 
 * 中国主要城市经纬度（用于真太阳时计算）
 */

export const CITIES = {
    // 直辖市
    '北京': { longitude: 116.4074, latitude: 39.9042, timezone: 8 },
    '上海': { longitude: 121.4737, latitude: 31.2304, timezone: 8 },
    '天津': { longitude: 117.1902, latitude: 39.1256, timezone: 8 },
    '重庆': { longitude: 106.5516, latitude: 29.5630, timezone: 8 },

    // 省会城市
    '石家庄': { longitude: 114.5149, latitude: 38.0428, timezone: 8 },
    '太原': { longitude: 112.5489, latitude: 37.8706, timezone: 8 },
    '呼和浩特': { longitude: 111.7490, latitude: 40.8423, timezone: 8 },
    '沈阳': { longitude: 123.4315, latitude: 41.8057, timezone: 8 },
    '长春': { longitude: 125.3235, latitude: 43.8171, timezone: 8 },
    '哈尔滨': { longitude: 126.5358, latitude: 45.8038, timezone: 8 },
    '南京': { longitude: 118.7969, latitude: 32.0603, timezone: 8 },
    '杭州': { longitude: 120.1551, latitude: 30.2741, timezone: 8 },
    '合肥': { longitude: 117.2272, latitude: 31.8206, timezone: 8 },
    '福州': { longitude: 119.2965, latitude: 26.0745, timezone: 8 },
    '南昌': { longitude: 115.8581, latitude: 28.6820, timezone: 8 },
    '济南': { longitude: 117.1205, latitude: 36.6510, timezone: 8 },
    '郑州': { longitude: 113.6254, latitude: 34.7466, timezone: 8 },
    '武汉': { longitude: 114.3055, latitude: 30.5931, timezone: 8 },
    '长沙': { longitude: 112.9388, latitude: 28.2282, timezone: 8 },
    '广州': { longitude: 113.2644, latitude: 23.1291, timezone: 8 },
    '南宁': { longitude: 108.3665, latitude: 22.8170, timezone: 8 },
    '海口': { longitude: 110.3312, latitude: 20.0318, timezone: 8 },
    '成都': { longitude: 104.0668, latitude: 30.5728, timezone: 8 },
    '贵阳': { longitude: 106.6302, latitude: 26.6477, timezone: 8 },
    '昆明': { longitude: 102.8329, latitude: 24.8801, timezone: 8 },
    '拉萨': { longitude: 91.1409, latitude: 29.6500, timezone: 8 },
    '西安': { longitude: 108.9402, latitude: 34.3416, timezone: 8 },
    '兰州': { longitude: 103.8343, latitude: 36.0611, timezone: 8 },
    '西宁': { longitude: 101.7782, latitude: 36.6171, timezone: 8 },
    '银川': { longitude: 106.2309, latitude: 38.4872, timezone: 8 },
    '乌鲁木齐': { longitude: 87.6168, latitude: 43.8256, timezone: 8 },

    // 特别行政区
    '香港': { longitude: 114.1694, latitude: 22.3193, timezone: 8 },
    '澳门': { longitude: 113.5439, latitude: 22.1987, timezone: 8 },

    // 其他主要城市
    '深圳': { longitude: 114.0579, latitude: 22.5431, timezone: 8 },
    '苏州': { longitude: 120.6191, latitude: 31.2990, timezone: 8 },
    '无锡': { longitude: 120.3119, latitude: 31.4912, timezone: 8 },
    '宁波': { longitude: 121.5440, latitude: 29.8683, timezone: 8 },
    '青岛': { longitude: 120.3826, latitude: 36.0671, timezone: 8 },
    '大连': { longitude: 121.6147, latitude: 38.9140, timezone: 8 },
    '厦门': { longitude: 118.0894, latitude: 24.4798, timezone: 8 },
    '温州': { longitude: 120.6994, latitude: 28.0006, timezone: 8 },
    '佛山': { longitude: 113.1214, latitude: 23.0218, timezone: 8 },
    '东莞': { longitude: 113.7518, latitude: 23.0207, timezone: 8 },
    '珠海': { longitude: 113.5769, latitude: 22.2700, timezone: 8 },
    '惠州': { longitude: 114.4160, latitude: 23.1115, timezone: 8 },
    '中山': { longitude: 113.3926, latitude: 22.5176, timezone: 8 },
    '汕头': { longitude: 116.6817, latitude: 23.3541, timezone: 8 },
    '台北': { longitude: 121.5654, latitude: 25.0330, timezone: 8 },
    '高雄': { longitude: 120.3014, latitude: 22.6273, timezone: 8 }
};

/**
 * 根据城市名获取经纬度
 * @param {string} cityName - 城市名
 * @returns {Object|null} 经纬度信息
 */
export function getCityLocation(cityName) {
    return CITIES[cityName] || null;
}

/**
 * 搜索城市
 * @param {string} keyword - 关键词
 * @returns {Array} 匹配的城市列表
 */
export function searchCities(keyword) {
    return Object.entries(CITIES)
        .filter(([name]) => name.includes(keyword))
        .map(([name, data]) => ({ name, ...data }));
}

/**
 * 获取所有城市列表
 * @returns {Array} 城市列表
 */
export function getAllCities() {
    return Object.entries(CITIES).map(([name, data]) => ({ name, ...data }));
}
