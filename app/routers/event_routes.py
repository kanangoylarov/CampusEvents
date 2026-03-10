from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from app.services import event_service
from app.repositories import organization_repository, room_repository, event_repository

event_bp = Blueprint('event', __name__)


def admin_required(f):
    """Yalnız admin keçə bilər."""
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please log in first.', 'danger')
            return redirect(url_for('user.login_form'))
        if current_user.role != 'admin':
            flash('You do not have permission to do this.', 'danger')
            return redirect(url_for('event.list_events'))
        return f(*args, **kwargs)
    return decorated


@event_bp.get('/events')
def list_events():
    raw_filters = {
        'org_id':      request.args.get('org_id', ''),
        'date_from':   request.args.get('date_from', ''),
        'date_to':     request.args.get('date_to', ''),
        'time_from':   request.args.get('time_from', ''),
        'time_to':     request.args.get('time_to', ''),
    }
    events = event_service.list_events(raw_filters)
    organizations = organization_repository.get_all_ordered_by_name()
    active_filters = any(v.strip() for v in raw_filters.values())
    return render_template(
        'events/index.html',
        events=events,
        organizations=organizations,
        filters=raw_filters,
        active_filters=active_filters,
    )


# ── Yalnız admin ──────────────────────────────────────────
@event_bp.get('/events/create')
@admin_required
def create_event_form():
    organizations = organization_repository.get_all_ordered_by_name()
    rooms = room_repository.get_all_ordered_by_name()
    return render_template('events/create.html',
                           organizations=organizations, rooms=rooms)


@event_bp.post('/events/create')
@admin_required
def create_event():
    event, error = event_service.create_event(
        request.form, request.files.get('picture'))
    if error:
        flash(error, 'danger')
        organizations = organization_repository.get_all_ordered_by_name()
        rooms = room_repository.get_all_ordered_by_name()
        return render_template('events/create.html',
                               organizations=organizations, rooms=rooms)
    flash('Event created successfully!', 'success')
    return redirect(url_for('event.list_events'))


@event_bp.get('/events/<int:id>/edit')
@admin_required
def update_event_form(id):
    event = event_repository.get_by_id(id)
    organizations = organization_repository.get_all_ordered_by_name()
    rooms = room_repository.get_all_ordered_by_name()
    return render_template('events/edit.html', event=event,
                           organizations=organizations, rooms=rooms)


@event_bp.post('/events/<int:id>/edit')
@admin_required
def update_event(id):
    event, error = event_service.update_event(
        id, request.form, request.files.get('picture'))
    if error:
        flash(error, 'danger')
        organizations = organization_repository.get_all_ordered_by_name()
        rooms = room_repository.get_all_ordered_by_name()
        return render_template('events/edit.html', event=event,
                               organizations=organizations, rooms=rooms)
    flash('Event updated successfully!', 'success')
    return redirect(url_for('event.list_events'))


@event_bp.post('/events/<int:id>/delete')
@admin_required
def delete_event(id):
    event_service.delete_event(id)
    flash('Event deleted successfully!', 'success')
    return redirect(url_for('event.list_events'))


# ── Yalnız login olmuş user ───────────────────────────────
@event_bp.post('/events/<int:id>/register')
@login_required
def register_event(id):
    event = event_repository.get_by_id(id)
    if not event:
        flash('Event not found.', 'danger')
        return redirect(url_for('event.list_events'))
    flash(f'Successfully registered for "{event.name}"!', 'success')
    return redirect(url_for('event.list_events'))