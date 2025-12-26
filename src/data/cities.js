/**
 * 城市数据（精简版）
 * 
 * 仅保留核心逻辑，数据已迁移至 public/cities.json
 */

/**
 * 获取城市数据的逻辑已移至前端静态加载
 */

export function getCityLocation(cityName) {
    // 后端不再维护完整的城市列表，如果必须在后端获取，需要重新设计
    // 但目前所有的坐标获取都移交给了前端，后端只负责接收 longitude/latitude
    return null;
}

export function searchCities(keyword) {
    return [];
}

export function getAllCities() {
    return [];
}

export const CITY_HIERARCHY = [];
