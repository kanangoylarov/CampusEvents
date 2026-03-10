from flask import Flask, request, redirect, url_for, flash
from flask_login import current_user

from app.extensions import db, login_manager
from app.config import config_by_name
from app.jwt_utils import decode_token

# No JWT needed
PUBLIC_ENDPOINTS = {
    'user.login_form', 'user.login',
    'user.register_form', 'user.register',
    'static',
}

# All logged-in users (user, organization, admin)
ALL_ROLES_ENDPOINTS = {
    'main.index',
    'user.logout',
    'event.list_events',
}

# organization + admin
ORG_ENDPOINTS = {
    'event.create_event_form', 'event.create_event',
    'event.update_event_form', 'event.update_event',
    'event.delete_event',
}

# admin only (room, organization CRUD, admin panel) — everything else


def create_app(config_name='development'):
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config.from_object(config_by_name[config_name])

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)

    # Register blueprints
    from app.routers.main import main_bp
    from app.routers.user_routes import user_bp
    from app.routers.event_routes import event_bp
    from app.routers.organization_routes import organization_bp
    from app.routers.room_routes import room_bp
    from app.routers.admin_routes import admin_bp

    for bp in [main_bp, user_bp, event_bp, organization_bp, room_bp, admin_bp]:
        app.register_blueprint(bp)

    @app.before_request
    def require_jwt_and_role():
        endpoint = request.endpoint

        # Public pages — no auth needed
        if endpoint in PUBLIC_ENDPOINTS:
            return

        # JWT check — must be logged in
        token = request.cookies.get('jwt_token')
        if not token or decode_token(token) is None:
            flash('Please log in to access this page.', 'danger')
            return redirect(url_for('user.login_form'))

        # All logged-in users can access these
        if endpoint in ALL_ROLES_ENDPOINTS:
            return

        role = current_user.role if current_user.is_authenticated else None

        # admin can access everything
        if role == 'admin':
            return

        # organization can access event CRUD
        if role == 'organization' and endpoint in ORG_ENDPOINTS:
            return

        # user role or organization accessing non-allowed page
        if role in ('user', 'organization'):
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('main.index'))

        # Fallback
        flash('Access denied.', 'danger')
        return redirect(url_for('user.login_form'))

    # Create all tables if they don't exist
    with app.app_context():
        db.create_all()

    return app
