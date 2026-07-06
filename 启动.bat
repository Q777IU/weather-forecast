@echo off
chcp 65001 >nul
title 天气预报程序

echo ============================================
echo    天气预报程序启动中...
echo ============================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到Python，请先安装Python 3.8以上版本
    echo 下载地址: https://www.python.org/downloads/
    echo 安装时请勾选 "Add Python to PATH"
    pause
    exit /b 1
)

REM 安装依赖
echo [1/2] 正在检查并安装依赖包...
pip install flask requests -q -i https://pypi.tuna.tsinghua.edu.cn/simple

REM 启动程序
echo [2/2] 正在启动天气预报程序...
echo.
echo 浏览器将自动打开，请勿关闭此窗口
echo 访问地址: http://127.0.0.1:5003
echo ============================================
echo.

python run.py

pause
