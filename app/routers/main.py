from flask import Blueprint, render_template

from app.services import event_service

main_bp = Blueprint('main', __name__)


@main_bp.get('/')
def index():
    events = event_service.list_events({})
    return render_template('main/index.html', events=events)
