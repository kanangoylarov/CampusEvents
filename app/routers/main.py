from flask import Blueprint, render_template

from app.repositories import event_repository

main_bp = Blueprint('main', __name__)


@main_bp.get('/')
def index():
    events = event_repository.filter_events()
    return render_template('main/index.html', events=events)
