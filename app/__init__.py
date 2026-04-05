from flask import Flask, request
from flask_login import current_user, login_user

from app.extensions import db, login_manager
from app.config import config_by_name
from app.jwt_utils import decode_token


class CurrentUser:
    """Replacement for Flask-Login's current_user for JWT-based auth."""
    def __init__(self, user=None):
        self.user = user
        self.is_authenticated = user is not None

    @property
    def full_name(self):
        return self.user.full_name if self.user else ""


def create_app(config_name='development'):
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config.from_object(config_by_name[config_name])

    # Initialize extensions
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

        user = User.query.get(user_id)
        if user:
            login_user(user)

    # Template context processor for JWT-based user info
    @app.context_processor
    def inject_current_user():
        return {'current_user': CurrentUser(current_user if current_user.is_authenticated else None)}

    # Register blueprints
    from app.routers.main import main_bp
    from app.routers.user_routes import user_bp
    from app.routers.event_routes import event_bp
    from app.routers.organization_routes import organization_bp
    from app.routers.room_routes import room_bp
    from app.routers.admin_routes import admin_bp

    for bp in [main_bp, user_bp, event_bp, organization_bp, room_bp, admin_bp]:
        app.register_blueprint(bp)

    # Create all tables and seed admin user if needed
    with app.app_context():
        try:
            db.create_all()
        except Exception:
            pass
        _seed_admin(app)

    return app


def _seed_admin(app):
    from app.models.user_model import User
    from werkzeug.security import generate_password_hash
    import os

    try:
        if User.query.filter_by(role='admin').first():
            return

        admin = User(
            full_name=os.environ.get('ADMIN_NAME', 'Admin'),
            email=os.environ.get('ADMIN_EMAIL', 'admin@admin.com'),
            password=generate_password_hash(os.environ.get('ADMIN_PASSWORD', 'admin123')),
            role='admin',
        )
        db.session.add(admin)
        db.session.commit()
    except Exception:
        db.session.rollback()
