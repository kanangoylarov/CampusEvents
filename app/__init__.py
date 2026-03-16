from flask import Flask, request
from flask_login import current_user, login_user

from app.extensions import db, login_manager
from app.config import config_by_name
from app.jwt_utils import decode_token


def create_app(config_name='development'):
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config.from_object(config_by_name[config_name])

    db.init_app(app)
    login_manager.init_app(app)

    @app.before_request
    def login_from_jwt_cookie():
        if current_user.is_authenticated:
            return
        token = request.cookies.get('jwt_token')
        if not token:
            return
        user_id = decode_token(token)
        if not user_id:
            return
        from app.models.user_model import User
        user = db.session.get(User, user_id)
        if user:
            login_user(user)

    from app.routers.main import main_bp
    from app.routers.user_routes import user_bp
    from app.routers.event_routes import event_bp
    from app.routers.organization_routes import organization_bp
    from app.routers.room_routes import room_bp
    from app.routers.admin_routes import admin_bp

    for bp in [main_bp, user_bp, event_bp, organization_bp, room_bp, admin_bp]:
        app.register_blueprint(bp)

    with app.app_context():
        db.create_all()

    return app
