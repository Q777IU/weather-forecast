import sys
import os
from flask import Flask, render_template, jsonify, request
from weather_analysis.weather_cn_api import get_weather_all, search_city, get_city_list
from weather_analysis.mock_data import generate_mock_weather_all, search_city_mock
from weather_analysis.analyzer import get_full_analysis

# 兼容PyInstaller打包后的路径
if getattr(sys, 'frozen', False):
    # 打包后的exe运行环境
    base_dir = sys._MEIPASS
else:
    # 开发环境
    base_dir = os.path.abspath(os.path.dirname(__file__))

template_dir = os.path.join(base_dir, 'templates')
app = Flask(__name__, template_folder=template_dir)


@app.route('/')
def index():
    return render_template('weather_index.html')


@app.route('/api/weather')
def weather():
    city = request.args.get('city', '北京')
    
    data = get_weather_all(city)
    
    if "error" in data:
        data = generate_mock_weather_all(city)
    
    analysis = get_full_analysis(
        data["current"],
        data["daily"],
        data["hourly"],
        data["air_quality"],
        data.get("indices", [])
    )
    
    result = {
        "city": data["city"],
        "data_source": data["data_source"],
        "current": {
            "city": data["current"].city,
            "temp": data["current"].temp,
            "feels_like": data["current"].feels_like,
            "text": data["current"].text,
            "wind_dir": data["current"].wind_dir,
            "wind_speed": data["current"].wind_speed,
            "humidity": data["current"].humidity,
            "pressure": data["current"].pressure,
            "vis": data["current"].vis,
            "uv_index": data["current"].uv_index,
            "aqi": data["current"].aqi,
            "aqi_level": data["current"].aqi_level,
            "pm25": data["current"].pm25,
            "pm10": data["current"].pm10,
            "update_time": data["current"].update_time.isoformat() if data["current"].update_time else None
        },
        "daily": [{
            "date": d.date,
            "temp_max": d.temp_max,
            "temp_min": d.temp_min,
            "text_day": d.text_day,
            "text_night": d.text_night,
            "wind_dir_day": d.wind_dir_day,
            "wind_speed_day": d.wind_speed_day,
            "humidity": d.humidity,
            "uv_index": d.uv_index,
            "sunrise": d.sunrise,
            "sunset": d.sunset
        } for d in data["daily"]],
        "hourly": [{
            "time": h.time,
            "temp": h.temp,
            "text": h.text,
            "wind_dir": h.wind_dir,
            "wind_speed": h.wind_speed,
            "humidity": h.humidity,
            "pop": h.pop
        } for h in data["hourly"]],
        "air_quality": {
            "aqi": data["air_quality"].aqi,
            "level": data["air_quality"].level,
            "category": data["air_quality"].category,
            "pm25": data["air_quality"].pm25,
            "pm10": data["air_quality"].pm10,
            "no2": data["air_quality"].no2,
            "so2": data["air_quality"].so2,
            "co": data["air_quality"].co,
            "o3": data["air_quality"].o3
        } if data["air_quality"] else None,
        "indices": [{
            "name": i.name,
            "level": i.level,
            "text": i.text
        } for i in data.get("indices", [])],
        "analysis": analysis
    }
    
    return jsonify(result)


@app.route('/api/search')
def search():
    keyword = request.args.get('keyword', '')
    
    cities = search_city(keyword)
    
    if not cities:
        cities = search_city_mock(keyword)
    
    return jsonify(cities)


@app.route('/api/cities')
def cities():
    return jsonify(get_city_list())


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5003)