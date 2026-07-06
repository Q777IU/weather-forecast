import requests
from datetime import datetime
from typing import List, Optional
from .models import (
    CurrentWeather, DailyForecast, HourlyWeather,
    AirQuality, WeatherIndices
)

QWEATHER_API_BASE = "https://devapi.qweather.com/v7"
QWEATHER_GEO_BASE = "https://geoapi.qweather.com/v2"

DEFAULT_KEY = "YOUR_API_KEY"


def search_city(location: str, key: str = DEFAULT_KEY) -> List[dict]:
    url = f"{QWEATHER_GEO_BASE}/city/lookup"
    params = {
        "location": location,
        "key": key,
        "number": 10
    }
    
    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        if data.get("code") == "200":
            return data.get("location", [])
        return []
    except Exception as e:
        print(f"Error searching city: {e}")
        return []


def get_current_weather(location_id: str, key: str = DEFAULT_KEY) -> Optional[CurrentWeather]:
    url = f"{QWEATHER_API_BASE}/weather/now"
    params = {"location": location_id, "key": key}
    
    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        if data.get("code") == "200" and data.get("now"):
            now = data["now"]
            return CurrentWeather(
                city="",
                city_id=location_id,
                temp=float(now["temp"]),
                feels_like=float(now["feelsLike"]),
                text=now["text"],
                wind_dir=now["windDir"],
                wind_speed=float(now["windSpeed"]),
                humidity=int(now["humidity"]),
                pressure=float(now["pressure"]),
                vis=float(now["vis"]),
                uv_index=float(now.get("uvIndex", 0)),
                update_time=datetime.fromisoformat(data["updateTime"].replace("Z", "+00:00"))
            )
        return None
    except Exception as e:
        print(f"Error fetching current weather: {e}")
        return None


def get_daily_forecast(location_id: str, days: int = 7, key: str = DEFAULT_KEY) -> List[DailyForecast]:
    url = f"{QWEATHER_API_BASE}/weather/{days}d"
    params = {"location": location_id, "key": key}
    
    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        if data.get("code") == "200" and data.get("daily"):
            forecasts = []
            for day in data["daily"]:
                forecasts.append(DailyForecast(
                    date=day["fxDate"],
                    temp_max=float(day["tempMax"]),
                    temp_min=float(day["tempMin"]),
                    text_day=day["textDay"],
                    text_night=day["textNight"],
                    wind_dir_day=day["windDirDay"],
                    wind_speed_day=float(day["windSpeedDay"]),
                    humidity=int(day["humidity"]),
                    uv_index=float(day["uvIndex"]),
                    moon_phase=day.get("moonPhase", ""),
                    sunrise=day.get("sunrise", ""),
                    sunset=day.get("sunset", "")
                ))
            return forecasts
        return []
    except Exception as e:
        print(f"Error fetching daily forecast: {e}")
        return []


def get_hourly_forecast(location_id: str, hours: int = 24, key: str = DEFAULT_KEY) -> List[HourlyWeather]:
    url = f"{QWEATHER_API_BASE}/weather/{hours}h"
    params = {"location": location_id, "key": key}
    
    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        if data.get("code") == "200" and data.get("hourly"):
            hourly = []
            for h in data["hourly"]:
                hourly.append(HourlyWeather(
                    time=h["fxTime"],
                    temp=float(h["temp"]),
                    text=h["text"],
                    wind_dir=h["windDir"],
                    wind_speed=float(h["windSpeed"]),
                    humidity=int(h["humidity"]),
                    pop=int(h.get("pop", 0))
                ))
            return hourly
        return []
    except Exception as e:
        print(f"Error fetching hourly forecast: {e}")
        return []


def get_air_quality(location_id: str, key: str = DEFAULT_KEY) -> Optional[AirQuality]:
    url = f"{QWEATHER_API_BASE}/air/now"
    params = {"location": location_id, "key": key}
    
    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        if data.get("code") == "200" and data.get("now"):
            now = data["now"]
            return AirQuality(
                aqi=int(now["aqi"]),
                level=now["level"],
                category=now["category"],
                pm25=float(now["pm2p5"]),
                pm10=float(now["pm10"]),
                no2=float(now["no2"]),
                so2=float(now["so2"]),
                co=float(now["co"]),
                o3=float(now["o3"]),
                update_time=datetime.fromisoformat(data["updateTime"].replace("Z", "+00:00"))
            )
        return None
    except Exception as e:
        print(f"Error fetching air quality: {e}")
        return None


def get_weather_indices(location_id: str, key: str = DEFAULT_KEY) -> List[WeatherIndices]:
    url = f"{QWEATHER_API_BASE}/indices/1d"
    params = {"location": location_id, "key": key, "type": "1,2,3,5,8,9"}
    
    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        if data.get("code") == "200" and data.get("daily"):
            indices = []
            for idx in data["daily"]:
                indices.append(WeatherIndices(
                    name=idx["name"],
                    level=idx["level"],
                    text=idx["text"],
                    category=idx["category"]
                ))
            return indices
        return []
    except Exception as e:
        print(f"Error fetching weather indices: {e}")
        return []


def get_weather_all(city_name: str, key: str = DEFAULT_KEY) -> dict:
    cities = search_city(city_name, key)
    
    if not cities:
        return {"error": "城市未找到", "cities": []}
    
    city = cities[0]
    location_id = city["id"]
    city_name_full = city["name"]
    
    current = get_current_weather(location_id, key)
    daily = get_daily_forecast(location_id, 7, key)
    hourly = get_hourly_forecast(location_id, 24, key)
    aqi = get_air_quality(location_id, key)
    indices = get_weather_indices(location_id, key)
    
    if current:
        current.city = city_name_full
        if aqi:
            current.aqi = aqi.aqi
            current.aqi_level = aqi.category
            current.pm25 = aqi.pm25
            current.pm10 = aqi.pm10
    
    return {
        "city": city_name_full,
        "city_id": location_id,
        "current": current,
        "daily": daily,
        "hourly": hourly,
        "air_quality": aqi,
        "indices": indices,
        "data_source": "qweather"
    }