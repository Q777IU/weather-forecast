import requests
from datetime import datetime, timedelta
from typing import List, Optional
from .models import CurrentWeather, DailyForecast, HourlyWeather, AirQuality, WeatherIndices

OPEN_METEO_API = "https://api.open-meteo.com/v1/forecast"

CITY_COORDS = {
    "北京": {"lat": 39.9042, "lon": 116.4074, "code": "101010100", "province": "北京"},
    "上海": {"lat": 31.2304, "lon": 121.4737, "code": "101020100", "province": "上海"},
    "广州": {"lat": 23.1291, "lon": 113.2644, "code": "101280101", "province": "广东"},
    "深圳": {"lat": 22.5431, "lon": 114.0579, "code": "101280601", "province": "广东"},
    "杭州": {"lat": 30.2741, "lon": 120.1551, "code": "101210101", "province": "浙江"},
    "成都": {"lat": 30.5728, "lon": 104.0668, "code": "101270101", "province": "四川"},
    "武汉": {"lat": 30.5928, "lon": 114.3055, "code": "101200101", "province": "湖北"},
    "西安": {"lat": 34.3416, "lon": 108.9398, "code": "101110101", "province": "陕西"},
    "南京": {"lat": 32.0603, "lon": 118.7969, "code": "101190101", "province": "江苏"},
    "重庆": {"lat": 29.4316, "lon": 106.9123, "code": "101040100", "province": "重庆"},
    "天津": {"lat": 39.0842, "lon": 117.2008, "code": "101030100", "province": "天津"},
    "苏州": {"lat": 31.2990, "lon": 120.5853, "code": "101190401", "province": "江苏"},
    "郑州": {"lat": 34.7466, "lon": 113.6253, "code": "101180101", "province": "河南"},
    "长沙": {"lat": 28.2280, "lon": 112.9388, "code": "101250101", "province": "湖南"},
    "青岛": {"lat": 36.0671, "lon": 120.3826, "code": "101120201", "province": "山东"},
    "宁波": {"lat": 29.8683, "lon": 121.5440, "code": "101210401", "province": "浙江"},
    "厦门": {"lat": 24.4798, "lon": 118.0894, "code": "101230201", "province": "福建"},
    "福州": {"lat": 26.0745, "lon": 119.2965, "code": "101230101", "province": "福建"},
    "沈阳": {"lat": 41.8057, "lon": 123.4315, "code": "101070101", "province": "辽宁"},
    "大连": {"lat": 38.9140, "lon": 121.6147, "code": "101070201", "province": "辽宁"},
    "哈尔滨": {"lat": 45.8038, "lon": 126.5350, "code": "101050101", "province": "黑龙江"},
    "长春": {"lat": 43.8171, "lon": 125.3235, "code": "101060101", "province": "吉林"},
    "济南": {"lat": 36.6512, "lon": 117.1201, "code": "101120101", "province": "山东"},
    "合肥": {"lat": 31.8206, "lon": 117.2272, "code": "101220101", "province": "安徽"},
    "南昌": {"lat": 28.6820, "lon": 115.8579, "code": "101240101", "province": "江西"},
    "南宁": {"lat": 22.8170, "lon": 108.3669, "code": "101300101", "province": "广西"},
    "贵阳": {"lat": 26.6470, "lon": 106.6302, "code": "101260101", "province": "贵州"},
    "昆明": {"lat": 25.0389, "lon": 102.7183, "code": "101290101", "province": "云南"},
    "拉萨": {"lat": 29.6500, "lon": 91.1000, "code": "101330101", "province": "西藏"},
    "兰州": {"lat": 36.0611, "lon": 103.8343, "code": "101160101", "province": "甘肃"},
    "西宁": {"lat": 36.6171, "lon": 101.7782, "code": "101150101", "province": "青海"},
    "银川": {"lat": 38.4872, "lon": 106.2309, "code": "101170101", "province": "宁夏"},
    "乌鲁木齐": {"lat": 43.8256, "lon": 87.6168, "code": "101130101", "province": "新疆"},
    "呼和浩特": {"lat": 40.8414, "lon": 111.7519, "code": "101080101", "province": "内蒙古"},
    "海口": {"lat": 20.0440, "lon": 110.1920, "code": "101310101", "province": "海南"},
    "三亚": {"lat": 18.2528, "lon": 109.5119, "code": "101310201", "province": "海南"},
    "石家庄": {"lat": 38.0428, "lon": 114.5149, "code": "101090101", "province": "河北"},
    "太原": {"lat": 37.8706, "lon": 112.5489, "code": "101100101", "province": "山西"},
    "无锡": {"lat": 31.4912, "lon": 120.3119, "code": "101190201", "province": "江苏"},
    "常州": {"lat": 31.8112, "lon": 119.9740, "code": "101190301", "province": "江苏"},
    "温州": {"lat": 27.9938, "lon": 120.6994, "code": "101210701", "province": "浙江"},
    "绍兴": {"lat": 30.0300, "lon": 120.5800, "code": "101210501", "province": "浙江"},
    "东莞": {"lat": 23.0489, "lon": 113.7447, "code": "101281601", "province": "广东"},
    "佛山": {"lat": 23.0218, "lon": 113.1219, "code": "101280800", "province": "广东"},
    "珠海": {"lat": 22.2707, "lon": 113.5767, "code": "101280701", "province": "广东"},
    "桂林": {"lat": 25.2736, "lon": 110.2900, "code": "101300501", "province": "广西"},
    "丽江": {"lat": 26.8721, "lon": 100.2299, "code": "101291401", "province": "云南"},
    "大理": {"lat": 25.6065, "lon": 100.2679, "code": "101290201", "province": "云南"}
}

WEATHER_CODES = {
    0: "晴",
    1: "晴",
    2: "多云",
    3: "阴",
    45: "雾",
    48: "雾",
    51: "毛毛雨",
    53: "小雨",
    55: "小雨",
    61: "小雨",
    63: "中雨",
    65: "大雨",
    71: "小雪",
    73: "中雪",
    75: "大雪",
    80: "阵雨",
    81: "阵雨",
    82: "雷阵雨",
    95: "雷阵雨",
    96: "雷阵雨",
    99: "雷阵雨"
}


def get_city_coord(city_name: str) -> dict:
    return CITY_COORDS.get(city_name, {"lat": 39.9042, "lon": 116.4074, "code": "101010100"})


def fetch_openmeteo(city_name: str) -> Optional[dict]:
    coords = get_city_coord(city_name)
    
    url = f"{OPEN_METEO_API}?latitude={coords['lat']}&longitude={coords['lon']}&current=temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m,wind_direction_10m&hourly=temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m,wind_direction_10m&daily=temperature_2m_max,temperature_2m_min,weather_code&forecast_days=7&timezone=Asia/Shanghai"
    
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        return data
    except Exception as e:
        print(f"Error fetching Open-Meteo: {e}")
        return None


def get_weather_text(code: int) -> str:
    return WEATHER_CODES.get(code, "晴")


def get_wind_direction(deg: float) -> str:
    directions = ["东风", "东北风", "北风", "西北风", "西风", "西南风", "南风", "东南风"]
    idx = round(deg / 45) % 8
    return directions[idx]


def parse_current_weather(city_name: str, data: dict) -> CurrentWeather:
    coords = get_city_coord(city_name)
    current = data.get("current", {})
    
    temp = current.get("temperature_2m", 25)
    humidity = current.get("relative_humidity_2m", 50)
    weather_code = current.get("weather_code", 0)
    wind_speed = current.get("wind_speed_10m", 2)
    wind_dir_deg = current.get("wind_direction_10m", 90)
    
    last_update = current.get("time", "")
    update_time = datetime.now()
    if last_update:
        try:
            update_time = datetime.fromisoformat(last_update.replace("Z", "+00:00"))
        except:
            pass
    
    return CurrentWeather(
        city=city_name,
        city_id=coords["code"],
        temp=round(temp, 1),
        feels_like=round(temp, 1),
        text=get_weather_text(weather_code),
        wind_dir=get_wind_direction(wind_dir_deg),
        wind_speed=round(wind_speed, 1),
        humidity=humidity,
        pressure=1013,
        vis=10,
        uv_index=0,
        aqi=50,
        aqi_level="良",
        pm25=35,
        pm10=55,
        update_time=update_time
    )


def parse_daily_forecast(data: dict) -> List[DailyForecast]:
    daily = []
    daily_data = data.get("daily", {})
    
    dates = daily_data.get("time", [])
    temps_max = daily_data.get("temperature_2m_max", [])
    temps_min = daily_data.get("temperature_2m_min", [])
    weather_codes = daily_data.get("weather_code", [])
    
    for i in range(min(len(dates), 7)):
        daily.append(DailyForecast(
            date=dates[i],
            temp_max=round(temps_max[i], 1),
            temp_min=round(temps_min[i], 1),
            text_day=get_weather_text(weather_codes[i]),
            text_night=get_weather_text(weather_codes[i]),
            wind_dir_day="东风",
            wind_speed_day=2.0,
            humidity=60,
            uv_index=5.0,
            sunrise="06:00",
            sunset="18:30"
        ))
    
    return daily


def parse_hourly_forecast(data: dict) -> List[HourlyWeather]:
    hourly = []
    hourly_data = data.get("hourly", {})
    
    times = hourly_data.get("time", [])
    temps = hourly_data.get("temperature_2m", [])
    hums = hourly_data.get("relative_humidity_2m", [])
    codes = hourly_data.get("weather_code", [])
    speeds = hourly_data.get("wind_speed_10m", [])
    dirs = hourly_data.get("wind_direction_10m", [])
    
    for i in range(min(len(times), 24)):
        hourly.append(HourlyWeather(
            time=times[i] + "+08:00",
            temp=round(temps[i], 1),
            text=get_weather_text(codes[i]),
            wind_dir=get_wind_direction(dirs[i]) if dirs else "东风",
            wind_speed=round(speeds[i], 1) if speeds else 2.0,
            humidity=hums[i] if hums else 50,
            pop=0
        ))
    
    return hourly


def generate_air_quality(city_name: str) -> Optional[AirQuality]:
    base_aqi = {
        "北京": 80, "上海": 45, "广州": 35, "深圳": 30, "杭州": 45,
        "成都": 65, "武汉": 50, "西安": 75, "南京": 48, "重庆": 60
    }
    aqi = base_aqi.get(city_name, 50)
    
    if aqi <= 50:
        level = "1"
        category = "优"
    elif aqi <= 100:
        level = "2"
        category = "良"
    elif aqi <= 150:
        level = "3"
        category = "轻度污染"
    elif aqi <= 200:
        level = "4"
        category = "中度污染"
    else:
        level = "5"
        category = "重度污染"
    
    return AirQuality(
        aqi=aqi,
        level=level,
        category=category,
        pm25=round(aqi * 0.7, 1),
        pm10=round(aqi * 1.1, 1),
        no2=20,
        so2=10,
        co=1.0,
        o3=60,
        update_time=datetime.now()
    )


def generate_indices(city_name: str, current: CurrentWeather) -> List[WeatherIndices]:
    temp = current.temp
    humidity = current.humidity
    
    indices = []
    
    if temp > 30:
        indices.append(WeatherIndices(name="舒适度", level="不舒适", text="天气炎热，注意防暑降温", category="5"))
    elif temp > 25:
        indices.append(WeatherIndices(name="舒适度", level="较不舒适", text="天气较热，建议穿轻薄衣物", category="4"))
    elif temp > 18:
        indices.append(WeatherIndices(name="舒适度", level="舒适", text="天气舒适，适合户外活动", category="3"))
    elif temp > 10:
        indices.append(WeatherIndices(name="舒适度", level="较舒适", text="天气凉爽，注意添衣", category="2"))
    else:
        indices.append(WeatherIndices(name="舒适度", level="寒冷", text="天气寒冷，注意保暖", category="1"))
    
    if temp > 28:
        indices.append(WeatherIndices(name="穿衣", level="薄款", text="建议穿短袖或轻薄衣物", category="1"))
    elif temp > 18:
        indices.append(WeatherIndices(name="穿衣", level="适中", text="建议穿长袖或薄外套", category="2"))
    else:
        indices.append(WeatherIndices(name="穿衣", level="厚款", text="建议穿厚衣服或羽绒服", category="3"))
    
    if 20 <= temp <= 28 and humidity < 70:
        indices.append(WeatherIndices(name="运动", level="适宜", text="天气适宜，适合户外运动", category="1"))
    elif 15 <= temp <= 32:
        indices.append(WeatherIndices(name="运动", level="较适宜", text="适合轻度运动", category="2"))
    else:
        indices.append(WeatherIndices(name="运动", level="不宜", text="不宜剧烈运动", category="3"))
    
    if temp > 25:
        indices.append(WeatherIndices(name="紫外线", level="中等", text="紫外线中等，注意防晒", category="2"))
    else:
        indices.append(WeatherIndices(name="紫外线", level="弱", text="紫外线较弱", category="1"))
    
    if "雨" in current.text:
        indices.append(WeatherIndices(name="洗车", level="不宜", text="有雨，不宜洗车", category="3"))
    else:
        indices.append(WeatherIndices(name="洗车", level="适宜", text="天气晴朗，适合洗车", category="1"))
    
    if temp > 20 and "雨" not in current.text:
        indices.append(WeatherIndices(name="旅游", level="适宜", text="天气不错，适合出游", category="1"))
    else:
        indices.append(WeatherIndices(name="旅游", level="较适宜", text="天气一般，出行注意", category="2"))
    
    return indices


def get_weather_all(city_name: str) -> dict:
    data = fetch_openmeteo(city_name)
    
    if not data:
        return {"error": "无法获取天气数据"}
    
    current = parse_current_weather(city_name, data)
    daily = parse_daily_forecast(data)
    hourly = parse_hourly_forecast(data)
    aqi = generate_air_quality(city_name)
    indices = generate_indices(city_name, current)
    
    if aqi:
        current.aqi = aqi.aqi
        current.aqi_level = aqi.category
        current.pm25 = aqi.pm25
        current.pm10 = aqi.pm10
    
    return {
        "city": city_name,
        "city_id": current.city_id,
        "current": current,
        "daily": daily,
        "hourly": hourly,
        "air_quality": aqi,
        "indices": indices,
        "data_source": "open-meteo"
    }


def get_city_list() -> list:
    return [{"name": name, "id": info["code"]} for name, info in CITY_COORDS.items()]


def search_city(keyword: str) -> list:
    results = []
    for name, info in CITY_COORDS.items():
        if keyword in name:
            results.append({"name": name, "id": info["code"]})
    return results