from flask import Flask
from flask_jwt_extended import get_jwt_identity

from app.extensions import db, jwt
from app.config import config_by_name


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
    jwt.init_app(app)

    # Template context processor for JWT-based user info
    @app.context_processor
    def inject_current_user():
        try:
            user_id = get_jwt_identity()
            if user_id:
                from app.models.user_model import User
                user = User.query.get(user_id)
                return {'current_user': CurrentUser(user)}
        except Exception:
            pass
        return {'current_user': CurrentUser(None)}

    # Register blueprints
    from app.routers.main import main_bp
    from app.routers.user_routes import user_bp
    from app.routers.event_routes import event_bp
    from app.routers.organization_routes import organization_bp
    from app.routers.room_routes import room_bp

    for bp in [main_bp, user_bp, event_bp, organization_bp, room_bp]:
        app.register_blueprint(bp)

    # Create all tables if they don't exist
    with app.app_context():
        db.create_all()

    return app
