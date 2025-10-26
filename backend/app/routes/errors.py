# backend/app/routes/errors.py 錯誤處理路由
from flask import Blueprint, render_template

errors_bp = Blueprint("errors", __name__)

@errors_bp.app_errorhandler(400)
def bad_request_error(e):
    return render_template("error.html", code=400, message="錯誤的請求。"), 400
@errors_bp.app_errorhandler(401)
def unauthorized_error(e):
    return render_template("error.html", code=401, message="未經授權的訪問。"), 401
@errors_bp.app_errorhandler(403)
def forbidden_error(e):
    return render_template("error.html", code=403, message="您沒有權限訪問此頁面。"), 403
@errors_bp.app_errorhandler(404)
def not_found_error(e):
    return render_template("error.html", code=404, message="找不到此頁面。"), 404
@errors_bp.app_errorhandler(405)
def method_not_allowed_error(e):
    return render_template("error.html", code=405, message="不允許使用此方法。"), 405
@errors_bp.app_errorhandler(500)
def internal_error(e):
    return render_template("error.html", code=500, message="伺服器發生內部錯誤。"), 500

