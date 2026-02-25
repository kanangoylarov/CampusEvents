from flask import Flask

from app.extensions import db, login_manager
from app.config import config_by_name


def create_app(config_name='development'):
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config.from_object(config_by_name[config_name])

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)

    # Register blueprints
    from app.routers.main import main_bp
    from app.routers.user import user_bp
    from app.routers.event import event_bp
    from app.routers.organization import organization_bp
    from app.routers.room import room_bp

    for bp in [main_bp, user_bp, event_bp, organization_bp, room_bp]:
        app.register_blueprint(bp)

    # Create all tables if they don't exist
    with app.app_context():
        db.create_all()

    return app
