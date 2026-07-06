import random
from datetime import datetime, timedelta
from .models import (
    CurrentWeather, DailyForecast, HourlyWeather,
    AirQuality, WeatherIndices
)

CITIES = {
    "北京": {"id": "101010100", "base_temp": 28, "base_humidity": 45, "aqi_base": 65},
    "上海": {"id": "101020100", "base_temp": 32, "base_humidity": 70, "aqi_base": 45},
    "广州": {"id": "101280101", "base_temp": 35, "base_humidity": 80, "aqi_base": 35},
    "深圳": {"id": "101280601", "base_temp": 33, "base_humidity": 75, "aqi_base": 30},
    "杭州": {"id": "101210101", "base_temp": 31, "base_humidity": 65, "aqi_base": 40},
    "成都": {"id": "101270101", "base_temp": 26, "base_humidity": 70, "aqi_base": 55},
    "武汉": {"id": "101200101", "base_temp": 30, "base_humidity": 60, "aqi_base": 50},
    "西安": {"id": "101110101", "base_temp": 27, "base_humidity": 50, "aqi_base": 70},
    "南京": {"id": "101190101", "base_temp": 29, "base_humidity": 65, "aqi_base": 48},
    "重庆": {"id": "101040100", "base_temp": 28, "base_humidity": 75, "aqi_base": 60}
}

WEATHER_TEXTS = ["晴", "多云", "阴", "小雨", "雷阵雨", "阵雨", "晴间多云"]
WIND_DIRS = ["东风", "南风", "西风", "北风", "东南风", "西南风", "东北风", "西北风"]

INDICES_TEMPLATES = [
    {"name": "舒适度", "levels": ["舒适", "较舒适", "一般", "较不舒适", "不舒适"], 
     "texts": ["天气舒适，适宜外出", "天气较好，适合出门", "天气一般，注意防护", 
              "天气较热，注意防暑", "天气炎热，减少外出"]},
    {"name": "穿衣", "levels": ["薄款", "适中", "厚款"], 
     "texts": ["建议穿短袖", "建议穿薄外套", "建议穿厚衣服"]},
    {"name": "运动", "levels": ["适宜", "较适宜", "不宜"], 
     "texts": ["适宜户外运动", "适合轻度运动", "不宜户外运动"]},
    {"name": "紫外线", "levels": ["弱", "中等", "强", "很强"], 
     "texts": ["紫外线弱，无需防护", "紫外线中等，注意防晒", "紫外线强，做好防晒", "紫外线很强，避免外出"]},
    {"name": "洗车", "levels": ["适宜", "较适宜", "不宜"], 
     "texts": ["天气晴好，适宜洗车", "天气较好，适合洗车", "可能下雨，不宜洗车"]},
    {"name": "旅游", "levels": ["适宜", "较适宜", "一般"], 
     "texts": ["天气很好，适合旅游", "天气不错，可以出游", "天气一般，出行注意"]}
]


def generate_mock_current(city_name: str) -> CurrentWeather:
    city_data = CITIES.get(city_name, {"base_temp": 25, "base_humidity": 60, "aqi_base": 50})
    
    temp = city_data["base_temp"] + random.uniform(-3, 3)
    feels_like = temp + random.uniform(-2, 4)
    aqi = city_data["aqi_base"] + random.randint(-15, 25)
    
    if aqi <= 50:
        aqi_level = "优"
    elif aqi <= 100:
        aqi_level = "良"
    elif aqi <= 150:
        aqi_level = "轻度污染"
    elif aqi <= 200:
        aqi_level = "中度污染"
    else:
        aqi_level = "重度污染"
    
    return CurrentWeather(
        city=city_name,
        city_id=CITIES.get(city_name, {}).get("id", "unknown"),
        temp=round(temp, 1),
        feels_like=round(feels_like, 1),
        text=random.choice(WEATHER_TEXTS),
        wind_dir=random.choice(WIND_DIRS),
        wind_speed=round(random.uniform(1, 5), 1),
        humidity=city_data["base_humidity"] + random.randint(-10, 10),
        pressure=round(1013 + random.uniform(-5, 5), 1),
        vis=round(random.uniform(10, 30), 1),
        uv_index=round(random.uniform(2, 8), 1),
        aqi=aqi,
        aqi_level=aqi_level,
        pm25=round(aqi * 0.7 + random.uniform(-5, 5), 1),
        pm10=round(aqi * 1.1 + random.uniform(-5, 5), 1),
        update_time=datetime.now()
    )


def generate_mock_daily(city_name: str, days: int = 7) -> list:
    city_data = CITIES.get(city_name, {"base_temp": 25, "base_humidity": 60})
    base_temp = city_data["base_temp"]
    
    forecasts = []
    today = datetime.now()
    
    for i in range(days):
        date = (today + timedelta(days=i)).strftime("%Y-%m-%d")
        temp_max = base_temp + random.uniform(-2, 5)
        temp_min = temp_max - random.uniform(5, 10)
        text_day = random.choice(WEATHER_TEXTS)
        text_night = random.choice(WEATHER_TEXTS[:3])
        
        forecasts.append(DailyForecast(
            date=date,
            temp_max=round(temp_max, 1),
            temp_min=round(temp_min, 1),
            text_day=text_day,
            text_night=text_night,
            wind_dir_day=random.choice(WIND_DIRS),
            wind_speed_day=round(random.uniform(1, 5), 1),
            humidity=city_data["base_humidity"] + random.randint(-10, 10),
            uv_index=round(random.uniform(2, 8), 1),
            moon_phase=random.choice(["新月", "上弦月", "满月", "下弦月"]),
            sunrise="05:" + str(random.randint(0, 59)).zfill(2),
            sunset="19:" + str(random.randint(0, 59)).zfill(2)
        ))
    
    return forecasts


def generate_mock_hourly(city_name: str, hours: int = 24) -> list:
    city_data = CITIES.get(city_name, {"base_temp": 25, "base_humidity": 60})
    base_temp = city_data["base_temp"]
    
    hourly = []
    now = datetime.now()
    
    for i in range(hours):
        hour_time = now + timedelta(hours=i)
        hour = hour_time.hour
        
        temp_modifier = 0
        if 6 <= hour < 12:
            temp_modifier = (hour - 6) * 0.8
        elif 12 <= hour < 15:
            temp_modifier = 5
        elif 15 <= hour < 20:
            temp_modifier = 5 - (hour - 15) * 0.8
        else:
            temp_modifier = -3
        
        temp = base_temp + temp_modifier + random.uniform(-1, 1)
        pop = random.randint(0, 30) if "雨" in random.choice(WEATHER_TEXTS) else random.randint(0, 10)
        
        hourly.append(HourlyWeather(
            time=hour_time.strftime("%Y-%m-%dT%H:%M+08:00"),
            temp=round(temp, 1),
            text=random.choice(WEATHER_TEXTS),
            wind_dir=random.choice(WIND_DIRS),
            wind_speed=round(random.uniform(1, 4), 1),
            humidity=city_data["base_humidity"] + random.randint(-10, 10) - int(temp_modifier * 0.5),
            pop=pop
        ))
    
    return hourly


def generate_mock_air_quality(city_name: str) -> AirQuality:
    city_data = CITIES.get(city_name, {"aqi_base": 50})
    aqi = city_data["aqi_base"] + random.randint(-15, 25)
    aqi = max(10, min(250, aqi))
    
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
        pm25=round(aqi * 0.7 + random.uniform(-5, 5), 1),
        pm10=round(aqi * 1.1 + random.uniform(-5, 5), 1),
        no2=round(random.uniform(10, 40), 1),
        so2=round(random.uniform(5, 20), 1),
        co=round(random.uniform(0.5, 1.5), 2),
        o3=round(random.uniform(40, 120), 1),
        update_time=datetime.now()
    )


def generate_mock_indices(city_name: str) -> list:
    city_data = CITIES.get(city_name, {"base_temp": 25})
    temp = city_data["base_temp"]
    
    indices = []
    for idx in INDICES_TEMPLATES:
        name = idx["name"]
        
        if name == "舒适度":
            level_idx = min(int((temp - 20) / 4), len(idx["levels"]) - 1)
            level_idx = max(0, min(level_idx, len(idx["levels"]) - 1))
        elif name == "穿衣":
            level_idx = 0 if temp > 28 else 1 if temp > 18 else 2
        elif name == "运动":
            level_idx = 0 if 20 <= temp <= 28 else 1 if 15 <= temp <= 32 else 2
        elif name == "紫外线":
            level_idx = random.randint(0, 3)
        elif name == "洗车":
            level_idx = random.randint(0, 2)
        else:
            level_idx = random.randint(0, 2)
        
        indices.append(WeatherIndices(
            name=name,
            level=idx["levels"][level_idx],
            text=idx["texts"][level_idx],
            category=str(level_idx + 1)
        ))
    
    return indices


def generate_mock_weather_all(city_name: str) -> dict:
    current = generate_mock_current(city_name)
    daily = generate_mock_daily(city_name, 7)
    hourly = generate_mock_hourly(city_name, 24)
    aqi = generate_mock_air_quality(city_name)
    indices = generate_mock_indices(city_name)
    
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
        "data_source": "mock"
    }


def get_city_list() -> list:
    return [{"name": name, "id": data["id"]} for name, data in CITIES.items()]


def search_city_mock(keyword: str) -> list:
    results = []
    for name, data in CITIES.items():
        if keyword in name:
            results.append({"name": name, "id": data["id"], "adm1": "中国"})
    return results