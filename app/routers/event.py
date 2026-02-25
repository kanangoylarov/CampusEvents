from datetime import date, time
from flask import Blueprint, render_template, request, redirect, url_for, flash

from app.extensions import db
from app.models.event_model import Event
from app.models.organization_model import Organization
from app.models.room_model import Room

event_bp = Blueprint('event', __name__)


def _parse_date(value):
    """Convert 'YYYY-MM-DD' string to a Python date object, or None."""
    if not value:
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def _parse_time(value):
    """Convert 'HH:MM' string to a Python time object, or None."""
    if not value:
        return None
    try:
        parts = value.split(':')
        return time(int(parts[0]), int(parts[1]))
    except (ValueError, IndexError):
        return None


def _build_event_from_form(form):
    """Extract and return a new Event instance from submitted form data."""
    return Event(
        name=form.get('name'),
        description=form.get('description'),
        picture=form.get('picture'),
        private=form.get('private') == 'on',
        date=_parse_date(form.get('date')),
        for_registration=form.get('for_registration'),
        start_time=_parse_time(form.get('start_time')),
        end_time=_parse_time(form.get('end_time')),
        room_id=form.get('room_id') or None,
        capacity=form.get('capacity') or None,
        organization_id=form.get('organization_id') or None,
    )


@event_bp.route('/events')
def list_events():
    events = Event.query.order_by(Event.date.asc()).all()
    return render_template('events/index.html', events=events)


@event_bp.route('/events/create', methods=['GET', 'POST'])
def create_event():
    if request.method == 'POST':
        new_event = _build_event_from_form(request.form)
        db.session.add(new_event)
        db.session.commit()
        flash('Event created successfully!', 'success')
        return redirect(url_for('event.list_events'))

    organizations = Organization.query.order_by(Organization.name).all()
    rooms = Room.query.order_by(Room.room_name).all()
    return render_template('events/create.html', organizations=organizations, rooms=rooms)
