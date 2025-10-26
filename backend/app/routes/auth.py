# backend/app/routes/auth.py 認證/登入系統相關路由
from flask import Blueprint, redirect, request, session, jsonify, render_template
import requests
from ..config import Config

auth_bp = Blueprint("auth", __name__)
API = Config.DISCORD["API_BASE"]

@auth_bp.route("/login")
def login():
    q = (
        f"{API}/oauth2/authorize"
        f"?client_id={Config.DISCORD['CLIENT_ID']}"
        f"&redirect_uri={Config.DISCORD['REDIRECT_URI']}"
        f"&response_type=code&scope=identify+guilds"
    )
    return redirect(q)

@auth_bp.route("/callback")
def callback():
    code = request.args.get("code")
    if not code:
        return render_template("error.html", code=400, message="缺少授權碼。"), 400

    r = requests.post(
        f"{API}/oauth2/token",
        data={
            "client_id": Config.DISCORD["CLIENT_ID"],
            "client_secret": Config.DISCORD["CLIENT_SECRET"],
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": Config.DISCORD["REDIRECT_URI"],
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    r.raise_for_status()
    session["token"] = r.json()["access_token"]
    return redirect("/")

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect("/")
