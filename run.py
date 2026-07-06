"""天气预报程序启动入口"""
import webbrowser
import threading
import time
import sys
import os

def open_browser():
    """延迟2秒后自动打开浏览器"""
    time.sleep(2)
    webbrowser.open("http://127.0.0.1:5003")

def main():
    print("=" * 50)
    print("    天气预报程序启动中...")
    print("    浏览器将自动打开，请勿关闭此窗口")
    print("    访问地址: http://127.0.0.1:5003")
    print("=" * 50)
    
    # 启动浏览器
    threading.Thread(target=open_browser, daemon=True).start()
    
    # 启动Flask应用
    from app import app
    app.run(debug=False, host='0.0.0.0', port=5003)

if __name__ == '__main__':
    main()
