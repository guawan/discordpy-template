# backend/app/routes/servers.py
from flask import Blueprint, render_template, jsonify, redirect, session, abort
import requests
from ..config import Config
from ..discord_api import get_user_guilds, get_bot_guilds, get_guild

servers_bp = Blueprint("servers", __name__)
API_BASE = Config.DISCORD["API_BASE"]

@servers_bp.route("/")
def index():
    if "token" not in session:
        return redirect("/login")
    return render_template("servers.html")

@servers_bp.route("/api/servers")
def servers():
    token = session.get("token")
    if not token:
        return jsonify({"error": "未登入"}), 401

    try:
        user_info = requests.get(
            f"{API_BASE}/users/@me",
            headers={"Authorization": f"Bearer {token}"}
        ).json()
    except Exception:
        return render_template("error.html", code=500, message="無法連線至 Discord API。"), 500

    user_guilds = get_user_guilds()
    bot_guilds = get_bot_guilds()
    bot_ids = {g["id"] for g in bot_guilds}
    visible = [g for g in user_guilds if g["id"] in bot_ids]

    return jsonify({"user": user_info, "guilds": visible})

@servers_bp.route("/server/<guild_id>")
def detail(guild_id):
    r = get_guild(guild_id, with_counts=True)  # 改這裡

    if r.status_code == 404:
        return render_template("error.html", code=404, message="找不到指定伺服器或您沒有權限存取。"), 404
    elif r.status_code == 403:
        return render_template("error.html", code=403, message="您沒有權限查看此伺服器。"), 403
    elif r.status_code >= 500:
        return render_template("error.html", code=500, message="Discord API 發生內部錯誤。"), 500

    guild = r.json()

    # 若回傳中沒有 counts，手動補上
    if "approximate_member_count" not in guild:
        try:
            c = requests.get(
                f"{API_BASE}/guilds/{guild_id}?with_counts=true",
                headers={"Authorization": f"Bot {Config.DISCORD['BOT_TOKEN']}"}
            ).json()
            guild["approximate_member_count"] = c.get("approximate_member_count")
            guild["approximate_presence_count"] = c.get("approximate_presence_count")
        except Exception:
            pass

    return render_template("server_detail.html", guild=guild)

