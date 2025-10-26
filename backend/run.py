# backend/run.py 入口文件

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

# 0.0.0.0 表示接受所有網路介面的連線
# port=5000 設定應用程式監聽的埠號
# debug=False 開發者模式關閉  
# debug=true 開發者模式開啟