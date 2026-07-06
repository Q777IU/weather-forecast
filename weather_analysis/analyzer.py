from typing import List, Dict
from datetime import datetime
from .models import DailyForecast, HourlyWeather, CurrentWeather, AirQuality


def analyze_temperature_trend(daily: List[DailyForecast]) -> Dict:
    if not daily:
        return {"trend": "stable", "avg_temp": 0, "temp_range": 0}
    
    temps_max = [d.temp_max for d in daily]
    temps_min = [d.temp_min for d in daily]
    all_temps = temps_max + temps_min
    
    avg_temp = sum(all_temps) / len(all_temps)
    max_temp = max(temps_max)
    min_temp = min(temps_min)
    temp_range = max_temp - min_temp
    
    first_half = sum(temps_max[:3]) / 3
    last_half = sum(temps_max[-3:]) / 3
    change = last_half - first_half
    
    if change > 2:
        trend = "rising"
    elif change < -2:
        trend = "falling"
    else:
        trend = "stable"
    
    return {
        "trend": trend,
        "avg_temp": round(avg_temp, 1),
        "max_temp": round(max_temp, 1),
        "min_temp": round(min_temp, 1),
        "temp_range": round(temp_range, 1),
        "change": round(change, 1),
        "daily_max": temps_max,
        "daily_min": temps_min
    }


def analyze_humidity(daily: List[DailyForecast]) -> Dict:
    if not daily:
        return {"avg_humidity": 0, "level": "normal"}
    
    humidities = [d.humidity for d in daily]
    avg_humidity = sum(humidities) / len(humidities)
    
    if avg_humidity > 70:
        level = "潮湿"
    elif avg_humidity < 30:
        level = "干燥"
    else:
        level = "舒适"
    
    return {
        "avg_humidity": round(avg_humidity, 1),
        "level": level,
        "daily_humidity": humidities
    }


def analyze_air_quality(aqi_data: AirQuality) -> Dict:
    if not aqi_data:
        return {"level": "未知", "health_effects": ""}
    
    aqi = aqi_data.aqi
    
    if aqi <= 50:
        level = "优"
        health_effects = "空气质量令人满意，基本无空气污染"
        suggestion = "各类人群可正常活动"
    elif aqi <= 100:
        level = "良"
        health_effects = "空气质量可接受，某些污染物可能对极少数异常敏感人群健康有较弱影响"
        suggestion = "极少数异常敏感人群应减少户外活动"
    elif aqi <= 150:
        level = "轻度污染"
        health_effects = "易感人群症状有轻度加剧，健康人群出现刺激症状"
        suggestion = "儿童、老年人及心脏病、呼吸系统疾病患者应减少长时间、高强度的户外锻炼"
    elif aqi <= 200:
        level = "中度污染"
        health_effects = "进一步加剧易感人群症状，可能对健康人群心脏、呼吸系统有影响"
        suggestion = "儿童、老年人及心脏病、呼吸系统疾病患者避免长时间、高强度的户外锻炼，一般人群适量减少户外活动"
    else:
        level = "重度污染"
        health_effects = "心脏病和肺病患者症状显著加剧，运动耐受力降低，健康人群普遍出现症状"
        suggestion = "儿童、老年人和心脏病、肺病患者应停留在室内，停止户外运动，一般人群减少户外运动"
    
    return {
        "aqi": aqi,
        "level": level,
        "health_effects": health_effects,
        "suggestion": suggestion,
        "pm25": aqi_data.pm25,
        "pm10": aqi_data.pm10,
        "no2": aqi_data.no2,
        "so2": aqi_data.so2,
        "co": aqi_data.co,
        "o3": aqi_data.o3
    }


def calculate_comfort_index(current: CurrentWeather) -> Dict:
    temp = current.temp
    humidity = current.humidity
    wind_speed = current.wind_speed
    
    thi = temp - 0.55 * (1 - humidity / 100) * (temp - 14.5)
    
    if thi > 28:
        level = "闷热不舒适"
        recommendation = "建议开启空调，减少户外活动"
    elif thi > 24:
        level = "较不舒适"
        recommendation = "穿轻薄衣物，注意防晒"
    elif thi > 18:
        level = "舒适"
        recommendation = "天气舒适，适合户外活动"
    elif thi > 10:
        level = "较舒适"
        recommendation = "天气凉爽，适当增添衣物"
    elif thi > 0:
        level = "冷"
        recommendation = "注意保暖，减少户外活动"
    else:
        level = "寒冷"
        recommendation = "非常寒冷，注意防寒保暖"
    
    return {
        "comfort_index": round(thi, 1),
        "level": level,
        "recommendation": recommendation
    }


def analyze_wind(daily: List[DailyForecast]) -> Dict:
    if not daily:
        return {"avg_speed": 0, "dominant_dir": "未知"}
    
    speeds = [d.wind_speed_day for d in daily]
    avg_speed = sum(speeds) / len(speeds)
    
    dirs = [d.wind_dir_day for d in daily]
    dominant_dir = max(set(dirs), key=dirs.count)
    
    return {
        "avg_speed": round(avg_speed, 1),
        "dominant_dir": dominant_dir,
        "daily_speeds": speeds,
        "daily_dirs": dirs
    }


def analyze_hourly_trend(hourly: List[HourlyWeather]) -> Dict:
    if not hourly:
        return {"temps": [], "rain_prob": 0}
    
    temps = [h.temp for h in hourly]
    pops = [h.pop for h in hourly]
    times = [h.time for h in hourly]
    
    max_temp = max(temps)
    min_temp = min(temps)
    max_rain = max(pops)
    
    return {
        "hourly_temps": temps,
        "hourly_times": times,
        "hourly_pop": pops,
        "max_temp": round(max_temp, 1),
        "min_temp": round(min_temp, 1),
        "max_rain_prob": max_rain
    }


def generate_recommendations(current: CurrentWeather, daily: List[DailyForecast], 
                              aqi_data: AirQuality = None) -> List[str]:
    recommendations = []
    
    comfort = calculate_comfort_index(current)
    recommendations.append(f"体感舒适度：{comfort['level']}，{comfort['recommendation']}")
    
    if current.text in ["小雨", "雷阵雨", "阵雨", "中雨", "大雨"]:
        recommendations.append("今日有雨，出门记得带伞")
    
    if current.temp > 35:
        recommendations.append("高温天气，注意防暑降温，多喝水")
    elif current.temp < 0:
        recommendations.append("低温天气，注意防寒保暖")
    
    if aqi_data and aqi_data.aqi > 100:
        recommendations.append("空气质量欠佳，敏感人群减少外出，外出建议佩戴口罩")
    
    if current.uv_index > 6:
        recommendations.append("紫外线强烈，外出做好防晒措施")
    
    if current.wind_speed > 5:
        recommendations.append("风力较大，注意防风")
    
    if len(daily) >= 3:
        temp_trend = analyze_temperature_trend(daily)
        if temp_trend["trend"] == "rising":
            recommendations.append(f"未来几天气温将上升{temp_trend['change']}°C，注意增减衣物")
        elif temp_trend["trend"] == "falling":
            recommendations.append(f"未来几天气温将下降{abs(temp_trend['change'])}°C，注意保暖")
    
    return recommendations


def get_full_analysis(current, daily, hourly, air_quality=None, indices=None) -> Dict:
    return {
        "temperature_trend": analyze_temperature_trend(daily),
        "humidity_analysis": analyze_humidity(daily),
        "air_quality_analysis": analyze_air_quality(air_quality) if air_quality else None,
        "comfort_index": calculate_comfort_index(current),
        "wind_analysis": analyze_wind(daily),
        "hourly_trend": analyze_hourly_trend(hourly),
        "recommendations": generate_recommendations(current, daily, air_quality)
    }