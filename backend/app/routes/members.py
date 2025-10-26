# backend/app/routes/members.py 成員相關路由
from flask import Blueprint, jsonify, render_template, abort
from ..discord_api import get_guild_members, get_guild, BOT_TOKEN, Config
import requests

members_bp = Blueprint("members", __name__)

@members_bp.route("/server/<guild_id>/members")
def members(guild_id):
    r = get_guild_members(guild_id)

    # --- 統一錯誤處理 ---
    if r.status_code == 404:
        abort(404)
    elif r.status_code == 403:
        abort(403)
    elif r.status_code >= 500:
        abort(500)

    # --- 正常回傳 ---
    if r.status_code != 200:
        abort(400)

    members = r.json()
    guild_info = get_guild(guild_id).json()
    return render_template("members.html", guild=guild_info, members=members)

@members_bp.route("/api/guilds/<guild_id>/kick/<user_id>", methods=["POST"])
def kick(guild_id, user_id):
    r = requests.delete(
        f"{Config.DISCORD['API_BASE']}/guilds/{guild_id}/members/{user_id}",
        headers={"Authorization": f"Bot {BOT_TOKEN}"}
    )
    return jsonify({"success": r.status_code == 204})

@members_bp.route("/api/guilds/<guild_id>/ban/<user_id>", methods=["POST"])
def ban(guild_id, user_id):
    r = requests.put(
        f"{Config.DISCORD['API_BASE']}/guilds/{guild_id}/bans/{user_id}",
        headers={"Authorization": f"Bot {BOT_TOKEN}"},
        json={"delete_message_days": 1, "reason": "由後台封鎖"}
    )
    return jsonify({"success": r.status_code == 204})
