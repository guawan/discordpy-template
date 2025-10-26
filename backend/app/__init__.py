# backend/app/init.py 應用程式初始化
from flask import Flask, session
from .config import Config
from .routes.auth import auth_bp
from .routes.servers import servers_bp
from .routes.members import members_bp
from .routes.errors import errors_bp
def create_app():
    app = Flask(__name__, template_folder="templates")
    app.config.from_object(Config)

    @app.before_request
    def keep_session():
        session.permanent = True

    app.register_blueprint(auth_bp)
    app.register_blueprint(servers_bp)
    app.register_blueprint(members_bp)
    app.register_blueprint(errors_bp)
    return app
