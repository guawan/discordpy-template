import requests
from flask import session
from .config import Config

API = Config.DISCORD["API_BASE"]
BOT_TOKEN = Config.DISCORD["BOT_TOKEN"]

def get_user_token():
    return session.get("token")

def auth_header(token=None):
    return {"Authorization": f"Bearer {token or get_user_token()}"}

def bot_header():
    return {"Authorization": f"Bot {BOT_TOKEN}"}

def get_user_guilds():
    """取得使用者加入的伺服器清單"""
    return requests.get(f"{API}/users/@me/guilds", headers=auth_header()).json()

def get_bot_guilds():
    """取得機器人加入的伺服器清單"""
    return requests.get(f"{API}/users/@me/guilds", headers=bot_header()).json()

def get_guild(guild_id, with_counts=False):
    """取得伺服器詳細資訊，可附帶成員/上線數"""
    url = f"{API}/guilds/{guild_id}"
    if with_counts:
        url += "?with_counts=true"
    return requests.get(url, headers=bot_header())

def get_guild_members(guild_id, limit=1000):
    """取得伺服器成員（最多1000）"""
    return requests.get(f"{API}/guilds/{guild_id}/members?limit={limit}", headers=bot_header())