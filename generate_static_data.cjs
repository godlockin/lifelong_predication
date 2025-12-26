const fs = require('fs');

const rawData = fs.readFileSync('china_cities.json', 'utf8');
const provinces = JSON.parse(rawData);

const hierarchy = [];
const flatCities = [];

provinces.forEach(prov => {
    const provinceNode = {
        name: prov.ProvinceNameZh,
        cities: []
    };

    prov.prefectureCities.forEach(pref => {
        const cityNode = {
            name: pref.prefectureNameZh,
            districts: []
        };

        pref.cities.forEach(city => {
            const districtName = city.nameZh;
            const lng = parseFloat(city.longtitude);
            const lat = parseFloat(city.latitude);

            // Add to hierarchy
            cityNode.districts.push({
                name: districtName,
                lng,
                lat
            });

            // Add to flat list for search
            // We want searchable items like:
            // "Chaoyang (Beijing)"
            // "Chaoyang (Liaoning)"
            // "Shijiazhuang"
            
            const fullName = `${prov.ProvinceNameZh} ${pref.prefectureNameZh} ${districtName}`;
            // If district name equals city name (usually the center), treat as city level search
            let displayName = districtName;
            let tags = [prov.ProvinceNameZh, pref.prefectureNameZh];
            
            if (districtName === pref.prefectureNameZh) {
                // City level
                tags = [prov.ProvinceNameZh];
            }
            
            flatCities.push({
                name: districtName,
                province: prov.ProvinceNameZh,
                city: pref.prefectureNameZh,
                full: fullName,
                lng,
                lat,
                tz: 8
            });
        });

        provinceNode.cities.push(cityNode);
    });

    hierarchy.push(provinceNode);
});

// Add special cities (HK, Macau, Taiwan) manually
const specialCities = [
    {
        name: '香港',
        cities: [{
            name: '香港',
            districts: [{ name: '香港', lng: 114.1694, lat: 22.3193 }]
        }]
    },
    {
        name: '澳门',
        cities: [{
            name: '澳门',
            districts: [{ name: '澳门', lng: 113.5439, lat: 22.1987 }]
        }]
    },
    {
        name: '台湾',
        cities: [
            {
                name: '台北',
                districts: [{ name: '台北', lng: 121.5654, lat: 25.0330 }]
            },
            {
                name: '高雄',
                districts: [{ name: '高雄', lng: 120.3014, lat: 22.6273 }]
            }
        ]
    }
];

specialCities.forEach(item => {
    // Add to hierarchy
    hierarchy.push(item);
    
    // Add to flat list
    item.cities.forEach(c => {
        c.districts.forEach(d => {
            flatCities.push({
                name: d.name,
                province: item.name,
                city: c.name,
                full: `${item.name} ${c.name} ${d.name}`,
                lng: d.lng,
                lat: d.lat,
                tz: 8
            });
        });
    });
});

const output = {
    hierarchy,
    flat: flatCities
};

fs.writeFileSync('public/cities.json', JSON.stringify(output));
console.log(`Processed ${hierarchy.length} provinces and ${flatCities.length} cities/districts.`);
