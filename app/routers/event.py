from datetime import date, time
from flask import Blueprint, render_template, request, redirect, url_for, flash

from app.extensions import db
from app.models.event_model import Event
from app.models.organization_model import Organization
from app.models.room_model import Room
from app.utils import cleanup_expired_events

event_bp = Blueprint('event', __name__)


def _room_has_conflict(room_id, event_date, new_start, new_end, exclude_id=None):
    """
    Return (True, conflicting_event) if the room is already booked for an
    overlapping time slot on the same date, otherwise (False, None).

    Overlap rule: A and B overlap when A.start < B.end AND B.start < A.end.
    If end_time is missing, it is treated as 23:59 (full remaining day).
    """
    if not room_id or not event_date:
        return False, None

    query = Event.query.filter(
        Event.room_id == int(room_id),
        Event.date == event_date,
    )
    if exclude_id:
        query = query.filter(Event.id != exclude_id)

    for existing in query.all():
        # No time info on either side → assume full-day conflict
        if existing.start_time is None or new_start is None:
            return True, existing

        existing_end = existing.end_time if existing.end_time else time(23, 59)
        new_end_safe = new_end if new_end else time(23, 59)

        if new_start < existing_end and existing.start_time < new_end_safe:
            return True, existing

    return False, None


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
    cleanup_expired_events()

    # Read filter params from query string
    org_id     = request.args.get('org_id', '').strip()
    date_from  = request.args.get('date_from', '').strip()
    date_to    = request.args.get('date_to', '').strip()
    time_from  = request.args.get('time_from', '').strip()
    time_to    = request.args.get('time_to', '').strip()

    query = Event.query

    if org_id:
        query = query.filter(Event.organization_id == int(org_id))

    if date_from:
        parsed = _parse_date(date_from)
        if parsed:
            query = query.filter(Event.date >= parsed)

    if date_to:
        parsed = _parse_date(date_to)
        if parsed:
            query = query.filter(Event.date <= parsed)

    if time_from:
        parsed = _parse_time(time_from)
        if parsed:
            query = query.filter(Event.start_time >= parsed)

    if time_to:
        parsed = _parse_time(time_to)
        if parsed:
            query = query.filter(Event.start_time <= parsed)

    events = query.order_by(Event.date.asc()).all()
    organizations = Organization.query.order_by(Organization.name).all()

    # Track whether any filter is active for the "clear" button
    active_filters = any([org_id, date_from, date_to, time_from, time_to])

    return render_template(
        'events/index.html',
        events=events,
        organizations=organizations,
        filters={
            'org_id': org_id,
            'date_from': date_from,
            'date_to': date_to,
            'time_from': time_from,
            'time_to': time_to,
        },
        active_filters=active_filters,
    )


@event_bp.route('/events/create', methods=['GET', 'POST'])
def create_event():
    if request.method == 'POST':
        room_id    = request.form.get('room_id') or None
        event_date = _parse_date(request.form.get('date'))
        start_time = _parse_time(request.form.get('start_time'))
        end_time   = _parse_time(request.form.get('end_time'))

        # Block booking if room is already taken for an overlapping slot
        if room_id and event_date:
            conflict, blocking = _room_has_conflict(room_id, event_date, start_time, end_time)
            if conflict:
                room = Room.query.get(int(room_id))
                start_str = blocking.start_time.strftime('%H:%M') if blocking.start_time else '?'
                end_str   = blocking.end_time.strftime('%H:%M')   if blocking.end_time   else 'end of day'
                flash(
                    f'Room "{room.room_name}" is already booked on {event_date} '
                    f'({start_str} – {end_str}) by "{blocking.name}". '
                    f'Choose a different room or a non-overlapping time slot.',
                    'danger'
                )
                organizations = Organization.query.order_by(Organization.name).all()
                rooms = Room.query.order_by(Room.room_name).all()
                return render_template('events/create.html',
                                       organizations=organizations, rooms=rooms)

        new_event = Event(
            name=request.form.get('name'),
            description=request.form.get('description'),
            picture=request.form.get('picture'),
            private=request.form.get('private') == 'on',
            date=event_date,
            for_registration=request.form.get('for_registration'),
            start_time=start_time,
            end_time=end_time,
            room_id=room_id,
            capacity=request.form.get('capacity') or None,
            organization_id=request.form.get('organization_id') or None,
        )
        db.session.add(new_event)
        db.session.commit()
        flash('Event created successfully!', 'success')
        return redirect(url_for('event.list_events'))

    organizations = Organization.query.order_by(Organization.name).all()
    rooms = Room.query.order_by(Room.room_name).all()
    return render_template('events/create.html', organizations=organizations, rooms=rooms)
