from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime


@dataclass
class CurrentWeather:
    city: str
    city_id: str
    temp: float
    feels_like: float
    text: str
    wind_dir: str
    wind_speed: float
    humidity: int
    pressure: float
    vis: float
    uv_index: float
    aqi: Optional[int] = None
    aqi_level: Optional[str] = None
    pm25: Optional[float] = None
    pm10: Optional[float] = None
    update_time: Optional[datetime] = None


@dataclass
class DailyForecast:
    date: str
    temp_max: float
    temp_min: float
    text_day: str
    text_night: str
    wind_dir_day: str
    wind_speed_day: float
    humidity: int
    uv_index: float
    moon_phase: str = ""
    sunrise: str = ""
    sunset: str = ""


@dataclass
class HourlyWeather:
    time: str
    temp: float
    text: str
    wind_dir: str
    wind_speed: float
    humidity: int
    pop: int = 0


@dataclass
class WeatherIndices:
    name: str
    level: str
    text: str
    category: str


@dataclass
class AirQuality:
    aqi: int
    level: str
    category: str
    pm25: float
    pm10: float
    no2: float
    so2: float
    co: float
    o3: float
    update_time: Optional[datetime] = None


@dataclass
class AnalysisResult:
    current: CurrentWeather
    daily: List[DailyForecast]
    hourly: List[HourlyWeather]
    air_quality: Optional[AirQuality]
    indices: List[WeatherIndices]
    trend_data: dict
    recommendations: List[str]