from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from app.services import event_service
from app.repositories import organization_repository, room_repository, event_repository


def _check_event_permission(event):
    """Return True if current user does NOT have permission to modify this event."""
    if current_user.role == 'admin':
        return False
    if current_user.role == 'user':
        flash('You do not have permission to do this.', 'danger')
        return True
    if current_user.role != 'organization':
        flash('You do not have permission to do this.', 'danger')
        return True
    if not event:
        flash('Event not found.', 'danger')
        return True
    user_org = current_user.organization_id
    event_org = event.organization_id
    if user_org and event_org and int(user_org) == int(event_org):
        return False
    flash('You can only modify your own organization\'s events.', 'danger')
    return True

event_bp = Blueprint('event', __name__)


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


# ── admin + organization (RBAC in __init__.py) ───────────
@event_bp.get('/events/create')
@login_required
def create_event_form():
    if current_user.role not in ('admin', 'organization'):
        flash('You do not have permission to do this.', 'danger')
        return redirect(url_for('event.list_events'))
    organizations = organization_repository.get_all_ordered_by_name()
    rooms = room_repository.get_all_ordered_by_name()
    return render_template('events/create.html',
                           organizations=organizations, rooms=rooms)


@event_bp.post('/events/create')
@login_required
def create_event():
    if current_user.role not in ('admin', 'organization'):
        flash('You do not have permission to do this.', 'danger')
        return redirect(url_for('event.list_events'))
    form_data = request.form.to_dict()
    if current_user.role == 'organization' and current_user.organization_id:
        form_data['organization_id'] = str(current_user.organization_id)
    event, error = event_service.create_event(
        form_data, request.files.get('picture'))
    if error:
        flash(error, 'danger')
        organizations = organization_repository.get_all_ordered_by_name()
        rooms = room_repository.get_all_ordered_by_name()
        return render_template('events/create.html',
                               organizations=organizations, rooms=rooms)
    flash('Event created successfully!', 'success')
    return redirect(url_for('event.list_events'))


@event_bp.get('/events/<int:id>/edit')
def update_event_form(id):
    event = event_repository.get_by_id(id)
    if _check_event_permission(event):
        return redirect(url_for('event.list_events'))
    organizations = organization_repository.get_all_ordered_by_name()
    rooms = room_repository.get_all_ordered_by_name()
    return render_template('events/edit.html', event=event,
                           organizations=organizations, rooms=rooms)


@event_bp.post('/events/<int:id>/edit')
def update_event(id):
    event = event_repository.get_by_id(id)
    if _check_event_permission(event):
        return redirect(url_for('event.list_events'))
    form_data = request.form.to_dict()
    if current_user.role == 'organization' and current_user.organization_id:
        form_data['organization_id'] = str(current_user.organization_id)
    event, error = event_service.update_event(
        id, form_data, request.files.get('picture'))
    if error:
        flash(error, 'danger')
        organizations = organization_repository.get_all_ordered_by_name()
        rooms = room_repository.get_all_ordered_by_name()
        return render_template('events/edit.html', event=event,
                               organizations=organizations, rooms=rooms)
    flash('Event updated successfully!', 'success')
    return redirect(url_for('event.list_events'))


@event_bp.post('/events/<int:id>/delete')
def delete_event(id):
    event = event_repository.get_by_id(id)
    if _check_event_permission(event):
        return redirect(url_for('event.list_events'))
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
