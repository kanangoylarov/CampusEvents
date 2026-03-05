from flask import Flask

from app.extensions import db, jwt
from app.config import config_by_name


def create_app(config_name='development'):
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config.from_object(config_by_name[config_name])

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)

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
