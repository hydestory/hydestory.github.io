import requests

authorization_code = "CWA-EB0C41B6-0482-40E4-8153-4330E46FECA9"
city_name = "臺北市"

def callWeatherAPI(authorization_code, city_name):
    url = f"https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization={authorization_code}&format=JSON&locationName={city_name}"

    try:
        # 向 API 發送請求
        response = requests.get(url)
        response.raise_for_status()  # 若請求有誤，將拋出 HTTPError
        
        # 解析 JSON 格式的回應
        data = response.json()
        
        # 嘗試從 JSON 中擷取天氣資訊
        records = data.get('records', {})
        locations = records.get('location', [])
        if not locations:
            # 若無法獲取位置資訊，拋出錯誤
            raise ValueError("Location data is empty")  
        
        # 返回結果
        return locations  
    
    # HTTP請求錯誤
    except requests.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  
    # 資料解析錯誤
    except ValueError as val_err:
        print(f"Data parsing error: {val_err}")  
    # 捕捉其他所有未預料的錯誤
    except Exception as err:
        print(f"An error occurred: {err}") 
    return None

# 天氣現象對應英文的字典
weather_translation = {
    "多雲": "Cloudy",
    "晴時多雲": "Partly cloudy",
    "晴天": "Sunny",
    "陰天": "Overcast",
    "雷陣雨": "Thunderstorms",
    "小雨": "Light rain",
    "大雨": "Heavy rain",
    "陣雨": "Showers",
    "雲量多": "Mostly cloudy",
    "大雷雨": "Severe thunderstorms",
    "小雪": "Light snow",
    "大雪": "Heavy snow",
    "冰雹": "Hail",
    "霧": "Fog",
    "霾": "Haze",
    "沙塵暴": "Sandstorm"
}

def translate_weather_condition(weather_condition):
    # 根據傳入的天氣現象返回對應的英文
    return weather_translation.get(weather_condition, "Unknown condition")

def extractWeatherInfo(weather_info):
    if not weather_info:
        return None

    # 提取天氣元素
    weather_elements = weather_info[0].get('weatherElement', [])

    # 創建字典以儲存需要的天氣資訊
    weather_data = {
        "max_temp": None,
        "min_temp": None,
        "weather": None,
        "rain_prob": None,
        "comfort_index": None
    }

    for element in weather_elements:
        if element["elementName"] == "MaxT":
            # 提取當天的最高溫資訊
            weather_data["max_temp"] = element["time"][0]["parameter"]["parameterName"]
        elif element["elementName"] == "MinT":
            # 提取當天的最低溫資訊
            weather_data["min_temp"] = element["time"][0]["parameter"]["parameterName"]
        elif element["elementName"] == "Wx":
            # 提取當天的天氣狀況
            chinese_weather = element["time"][0]["parameter"]["parameterName"]
            # 進行中文到英文的轉換
            weather_data["weather"] = translate_weather_condition(chinese_weather)
        elif element["elementName"] == "PoP":
            # 提取當天的降雨機率
            weather_data["rain_prob"] = element["time"][0]["parameter"]["parameterName"]
        elif element["elementName"] == "CI":
            # 提取當天的舒適度指數
            weather_data["comfort_index"] = element["time"][0]["parameter"]["parameterName"]

    return weather_data

if __name__ == "__main__":
    # 呼叫 callWeatherAPI 函數
    weather_info = callWeatherAPI(authorization_code, city_name)
    
    # 如果成功取得天氣資訊
    if weather_info:
        # 提取天氣資訊
        weather_data = extractWeatherInfo(weather_info)
        
        if weather_data:
            # 顯示今天的天氣資訊（英文）
            print(f"Today's Max Temperature: {weather_data['max_temp']}°C")
            print(f"Today's Min Temperature: {weather_data['min_temp']}°C")
            print(f"Today's Weather: {weather_data['weather']}")
            print(f"Today's Rain Probability: {weather_data['rain_prob']}%")
            print(f"Today's Comfort Index: {weather_data['comfort_index']}")
        else:
            print("Unable to extract weather data")
    else:
        print("Unable to get weather data")
