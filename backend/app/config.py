# backend/app/config.py 配置文件讀取
import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SESSION_PERMANENT = True
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = False  # HTTPS 時改 True

    DISCORD = {
        "CLIENT_ID": os.getenv("DISCORD_CLIENT_ID"),
        "CLIENT_SECRET": os.getenv("DISCORD_CLIENT_SECRET"),
        "REDIRECT_URI": os.getenv("OAUTH_REDIRECT_URI"),
        "BOT_TOKEN": os.getenv("DISCORD_BOT_TOKEN"),
        "API_BASE": "https://discord.com/api"
    }
