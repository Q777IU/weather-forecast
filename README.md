# 天气预报

一个基于 Flask 和 Open-Meteo API 的实时天气预报 Web 应用。

## 功能特点

- 🌤️ **实时天气数据**：使用 Open-Meteo API 获取全球实时天气数据
- 🏙️ **48个城市支持**：覆盖全国主要城市，支持搜索和快速切换
- 📊 **24小时温度趋势**：可视化图表展示逐小时温度变化
- 📅 **7日天气预报**：每日最高/最低温度和天气状况
- 🌡️ **空气质量**：AQI指数及6项污染物数据
- 🧑‍💼 **生活指数**：舒适度、穿衣、运动、紫外线、洗车、旅游建议
- 📱 **响应式设计**：支持手机、平板和桌面设备

## 技术栈

- **后端**: Python Flask
- **前端**: HTML5、CSS3、JavaScript
- **图表**: ECharts
- **数据源**: Open-Meteo API
- **部署**: 本地开发服务器

## 快速开始

### 安装依赖

```bash
pip install flask requests beautifulsoup4
```

### 运行应用

```bash
python app.py
```

### 访问网页

打开浏览器访问：http://127.0.0.1:5003

## 项目结构

```
weather-forecast/
├── app.py                    # Flask 应用入口
├── weather_analysis/         # 天气分析模块
│   ├── __init__.py
│   ├── models.py             # 数据模型
│   ├── weather_cn_api.py     # Open-Meteo API 接口
│   ├── qweather_api.py       # 和风天气 API 接口（备用）
│   ├── mock_data.py          # 模拟数据（备用）
│   └── analyzer.py           # 数据分析模块
├── templates/                # 前端模板
│   └── weather_index.html    # 主页面
└── README.md                 # 项目说明
```

## API 接口

### 获取天气数据

```
GET /api/weather?city=城市名称
```

**示例**:
```
GET /api/weather?city=北京
```

**返回**:
```json
{
    "city": "北京",
    "current": {
        "temp": 28.5,
        "text": "晴",
        "humidity": 45,
        "wind_speed": 3.2,
        "wind_dir": "东风"
    },
    "daily": [...],
    "hourly": [...],
    "air_quality": {...},
    "indices": [...]
}
```

### 获取城市列表

```
GET /api/cities
```

### 搜索城市

```
GET /api/search?keyword=关键词
```

## 数据来源

- **实时天气数据**: Open-Meteo API (https://open-meteo.com)
- **数据更新频率**: 每小时更新
- **访问方式**: 免费、无需 API Key

## 许可证

MIT License