// 天氣 API 整合
class WeatherIntegration {
    constructor() {
        this.apiKey = "CWA-EB0C41B6-0482-40E4-8153-4330E46FECA9";
        this.cityName = "臺北市";
        this.baseUrl = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001";
    }

    // 天氣現象翻譯字典
    weatherTranslation = {
        "多雲": "多雲",
        "晴時多雲": "晴時多雲", 
        "晴天": "晴天",
        "陰天": "陰天",
        "雷陣雨": "雷陣雨",
        "小雨": "小雨",
        "大雨": "大雨",
        "陣雨": "陣雨",
        "雲量多": "雲量多",
        "大雷雨": "大雷雨",
        "小雪": "小雪",
        "大雪": "大雪",
        "冰雹": "冰雹",
        "霧": "霧",
        "霾": "霾",
        "沙塵暴": "沙塵暴"
    };

    // 獲取天氣資料
    async fetchWeatherData() {
        try {
            const url = `${this.baseUrl}?Authorization=${this.apiKey}&format=JSON&locationName=${this.cityName}`;
            const response = await fetch(url);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            return this.parseWeatherData(data);
        } catch (error) {
            console.error('獲取天氣資料失敗:', error);
            return this.getFallbackWeatherData();
        }
    }

    // 解析天氣資料
    parseWeatherData(data) {
        try {
            const records = data.records || {};
            const locations = records.location || [];
            
            if (locations.length === 0) {
                throw new Error("Location data is empty");
            }

            const weatherElements = locations[0].weatherElement || [];
            const weatherData = {
                max_temp: null,
                min_temp: null,
                weather: null,
                rain_prob: null,
                comfort_index: null
            };

            weatherElements.forEach(element => {
                switch (element.elementName) {
                    case "MaxT":
                        weatherData.max_temp = element.time[0].parameter.parameterName;
                        break;
                    case "MinT":
                        weatherData.min_temp = element.time[0].parameter.parameterName;
                        break;
                    case "Wx":
                        weatherData.weather = element.time[0].parameter.parameterName;
                        break;
                    case "PoP":
                        weatherData.rain_prob = element.time[0].parameter.parameterName;
                        break;
                    case "CI":
                        weatherData.comfort_index = element.time[0].parameter.parameterName;
                        break;
                }
            });

            return weatherData;
        } catch (error) {
            console.error('解析天氣資料失敗:', error);
            return this.getFallbackWeatherData();
        }
    }

    // 備用天氣資料
    getFallbackWeatherData() {
        return {
            max_temp: "25",
            min_temp: "20",
            weather: "多雲",
            rain_prob: "30",
            comfort_index: "舒適"
        };
    }

    // 更新天氣顯示
    async updateWeatherDisplay() {
        const weatherData = await this.fetchWeatherData();
        
        // 更新溫度顯示
        const tempElement = document.getElementById('weather-temp');
        if (tempElement && weatherData.max_temp && weatherData.min_temp) {
            tempElement.textContent = `${weatherData.min_temp}°C - ${weatherData.max_temp}°C`;
        }

        // 更新天氣狀況
        const conditionElement = document.getElementById('weather-condition');
        if (conditionElement && weatherData.weather) {
            conditionElement.textContent = weatherData.weather;
        }

        // 更新詳細資訊
        const detailsElement = document.getElementById('weather-details');
        if (detailsElement) {
            let details = [];
            if (weatherData.rain_prob) {
                details.push(`降雨機率: ${weatherData.rain_prob}%`);
            }
            if (weatherData.comfort_index) {
                details.push(`舒適度: ${weatherData.comfort_index}`);
            }
            detailsElement.textContent = details.join(' | ');
        }
    }
}

// 應用程式使用統計整合
class AppUsageIntegration {
    constructor() {
        this.usageDataUrl = "src/text/usage_log.json";
    }

    // 獲取使用統計資料
    async fetchUsageData() {
        try {
            const response = await fetch(this.usageDataUrl);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            return this.parseUsageData(data);
        } catch (error) {
            console.error('獲取使用統計失敗:', error);
            return this.getFallbackUsageData();
        }
    }

    // 解析使用統計資料
    parseUsageData(data) {
        const totalSeconds = Object.values(data).reduce((sum, time) => sum + time, 0);
        const totalHours = Math.round((totalSeconds / 3600) * 10) / 10;
        
        const topApp = Object.entries(data).reduce((a, b) => data[a[0]] > data[b[0]] ? a : b, ['Unknown', 0]);
        const topAppName = topApp[0];

        return {
            totalHours: totalHours,
            topApp: topAppName,
            appCount: Object.keys(data).length
        };
    }

    // 備用使用統計資料
    getFallbackUsageData() {
        return {
            totalHours: 6.5,
            topApp: "Visual Studio Code",
            appCount: 8
        };
    }

    // 更新使用統計顯示
    async updateUsageDisplay() {
        const usageData = await this.fetchUsageData();
        
        const usageElement = document.getElementById('app-usage');
        if (usageElement) {
            usageElement.textContent = `${usageData.totalHours} 小時`;
        }

        const topAppElement = document.getElementById('top-app');
        if (topAppElement) {
            topAppElement.textContent = usageData.topApp;
        }
    }
}

// 學習進度整合
class LearningProgressIntegration {
    constructor() {
        this.noteCount = this.countNotes();
    }

    // 計算筆記數量
    countNotes() {
        // 這裡可以根據實際的筆記檔案結構來計算
        // 暫時返回模擬數據
        return 8;
    }

    // 獲取學習統計
    getLearningStats() {
        return {
            studyHours: 12, // 這裡可以從實際數據計算
            noteCount: this.noteCount
        };
    }

    // 更新學習進度顯示
    updateLearningDisplay() {
        const stats = this.getLearningStats();
        
        const studyHoursElement = document.getElementById('study-hours');
        if (studyHoursElement) {
            studyHoursElement.textContent = `${stats.studyHours} 小時`;
        }

        const noteCountElement = document.getElementById('note-count');
        if (noteCountElement) {
            noteCountElement.textContent = `${stats.noteCount} 篇`;
        }
    }
}

// 初始化所有整合功能
document.addEventListener('DOMContentLoaded', function() {
    const weatherIntegration = new WeatherIntegration();
    const appUsageIntegration = new AppUsageIntegration();
    const learningProgressIntegration = new LearningProgressIntegration();

    // 更新所有顯示
    weatherIntegration.updateWeatherDisplay();
    appUsageIntegration.updateUsageDisplay();
    learningProgressIntegration.updateLearningDisplay();

    // 每 5 分鐘更新一次天氣資料
    setInterval(() => {
        weatherIntegration.updateWeatherDisplay();
    }, 5 * 60 * 1000);

    // 每 10 分鐘更新一次使用統計
    setInterval(() => {
        appUsageIntegration.updateUsageDisplay();
    }, 10 * 60 * 1000);
});
