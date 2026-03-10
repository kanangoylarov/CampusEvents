<<<<<<< HEAD
from flask import Flask
from flask_jwt_extended import get_jwt_identity

from app.extensions import db, jwt
from app.config import config_by_name
=======
from flask import Flask, request
from flask_login import current_user, login_user

from app.extensions import db, login_manager
from app.config import config_by_name
from app.jwt_utils import decode_token
>>>>>>> origin/kanan


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
<<<<<<< HEAD
    jwt.init_app(app)
=======
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
>>>>>>> origin/kanan

    # Template context processor for JWT-based user info
    @app.context_processor
    def inject_current_user():
<<<<<<< HEAD
        try:
            user_id = get_jwt_identity()
            if user_id:
                from app.models.user_model import User
                user = User.query.get(user_id)
                return {'current_user': CurrentUser(user)}
        except Exception:
            pass
        return {'current_user': CurrentUser(None)}
=======
        return {'current_user': CurrentUser(current_user if current_user.is_authenticated else None)}
>>>>>>> origin/kanan

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
